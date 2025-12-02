# How to Implement Contracts

This page explains **how to go from “idea” to a working implementation** by wiring together the four main contracts:

* `Data` / `DataCore`
* `DataProcessor` / `DataProcessorCore`
* `DeviceWorker` / `DeviceWorkerCore`
* `Plotter` and its subclasses

plus their supporting pieces: `PlotterOptions`, widgets, and datasets.

This is the “how to implement it in code” companion to **How to think about this application?**. It assumes you’ve read that first and now want something more concrete.

---

## 1. Overview of the Contracts

### 1.1 `Data` / `DataCore` – reading files and exposing observables

The `Data` contract defines *how raw files are turned into named observables*.

Key responsibilities:

* Read one raw file (`self.file_reader(filepath)`).
* Store raw values internally (e.g. in `self.raw_data`).
* Provide values and units for each observable:

  * `get_data(observable)`
  * `get_units(observable)`
  * `get_allowed_observables()` (names you support)

`DataCore` implements all of this except `read_file`, and provides a standard internal format:

```python
self.raw_data[observable] = {"units": "...", "data": ...}
```

You normally **subclass `DataCore`**, implement `read_file`, and fill `self.raw_data`.

---

### 1.2 `DataProcessor` / `DataProcessorCore` – derived quantities

The `DataProcessor` contract defines *how you compute derived observables from raw data*.

Key responsibilities:

* `get_data(observable, *args, **kwargs)` – returns raw **or** processed data.
* `get_units(observable)` – units for any observable.
* `validate_observables(*args)` – sanity checks.
* Use a reference to a `Data` instance.

`DataProcessorCore`:

* Talks to `Data` for raw values.

* Contains a dictionary of processing functions:

  ```python
  self._processing_functions = {
      "elapsed_time": self.elapsed_time,
      # your functions here…
  }
  ```

* Caches results in `self.processed_data` to avoid recomputation.

You usually **subclass `DataProcessorCore`**, add entries to `_processing_functions`, and implement the corresponding methods.

---

### 1.3 `DeviceWorker` / `DeviceWorkerCore` – orchestrating the workflow

The `DeviceWorker` contract defines *how one device turns a dataset into one or more plots*, typically in a background thread.

Responsibilities:

* Know which `Data` and `DataProcessor` subclasses to use (`set_data_type`, `set_processor_type`).
* Read all files from a dataset and build a processor per file (`set_data(dataspec)`).
* Expose plot functions (named `plot_{something}`) that:

  * instantiate a plotter
  * call `ready_plot` with processors and options
  * call `draw_plot`

`DeviceWorkerCore` already:

* Manages Qt signals (`finished`, `progress`).
* Reads all files from a `DataSpec` into `self.data_processors`.
* Injects useful options (e.g. experiment datetime, colours) into `PlotterOptions`.

You generally **subclass `DeviceWorkerCore`**, set the types, and implement a few `plot_*` methods.

---

### 1.4 `Plotter` and its subclasses – turning processors into figures

The `Plotter` contract is minimal:

* `ready_plot(processors, options)` – configure everything.
* `draw_plot()` – actually build and show the figure.

Concrete plotters like `HeatmapPlotter`:

* Expect a mapping of keys → processors.
* Use `processor.get_data()` and `processor.get_units()` to get values and labels.
* Configure Plotly/Matplotlib objects and show them.

You can **reuse existing plotters** (scatter, heatmap, histogram, …) or implement your own when the visualisation is new.

---

### 1.5 `PlotterOptions` – options bridge

`PlotterOptions` is a simple key–value store for options coming from the GUI:

* `add_option(label, value)`
* `get_option(label)`
* `has_options(labels)`

The GUI builds this from widget elements with an `option_alias`. The worker passes it on to the plotter. Plotters read it to configure axes, ranges, log scales, etc.

---

## 2. Step-by-Step: Implementing All Contracts

We’ll implement a simple **IV device** that:

* reads two-column IV data (voltage, current),
* computes `voc` and `isc`,
* exposes two plots:

  * raw IV curve,
  * a small “parameters” view.

This mirrors the workflow you described in the “How to think about this application?” page.

---

### Step 0 – Decide what you want

Before touching code, answer:

1. **What do the files look like?**
   Two columns: `V` (voltage), `I` (current).

2. **What observables do I need?**
   Raw: `voltage`, `current`.
   Derived: `voc`, `isc`.

3. **What plots should the device offer?**

   * `plot_iv_curve`
   * `plot_iv_parameters`

4. **Which visualisation type fits?**

   * IV curve → scatter/line plot.
   * Parameters → maybe a simple text summary.

We’ll assume a generic **ScatterPlotter** already exists (similar in spirit to `HeatmapPlotter`).

---

### Step 1 – Implement the `Data` contract with a `DataCore` subclass

Create a class (e.g. `IVData`) that:

* subclasses `DataCore`,
* implements `read_file`,
* fills `self.raw_data` with the right observables.

Skeleton:

```python
from analysis.data.data_types.data_types import DataCore  # path adjusted to your project

class IVData(DataCore):
    def __init__(self, label):
        super().__init__(file_reader=read_two_column_file)
        self.raw_data = {
            "voltage": None,
            "current": None,
        }
        self._allowed_observables = self.raw_data.keys()
        
    def read_file(self, filepath: str) -> None:
        # 1. Reuse an existing reader (csv, etc.)
        file_results = self.file_reader(filepath)  # your reader

        # 2. Store observables using the standard structure
        if self.raw_data["voltage"] is None:
            self.raw_data["voltage"] = {"units": "V", "data": file_results['0']}
        if self.raw_data["current"] is None:
            self.raw_data["current"] = {"units": "A", "data": file_results['1']}
```

Notes:

* `DataCore.get_data`, `get_units`, and `get_allowed_observables` are already implemented for you.
* The important part is populating `self.raw_data` and `_allowed_observables`.

---

### Step 2 – Implement `DataProcessor` with a `DataProcessorCore` subclass

Next, create an `IVProcessor` that:

* uses your `IVData`,
* computes `voc` and `isc`,
* reuses the core behavior for everything else.

```python
from contracts.data_processors import DataProcessorCore
from implementations.data.data_types.iv_data import IVData

class IVProcessor(DataProcessorCore):
    def __init__(self, data: IVData):
        super().__init__(data)

        # Add your own processing functions
        self._processing_functions.update({
            "voc": self.compute_open_circuit_voltage,
            "isc": self.compute_short_circuit_current,
        })

        # Reset processed_data & keys after updating
        self.processed_data = {key: None for key in self._processing_functions}
        self._processed_observables = self.processed_data.keys()

    def compute_open_circuit_voltage(self):
        voltage = self.get_data("voltage")
        current = self.get_data("current")
        # Very naive example: find V where I is closest to 0
        idx = min(range(len(current)), key=lambda i: abs(current[i]))
        return {"units": "V", "data": voltage[idx]}

    def compute_short_circuit_current(self):
        voltage = self.get_data("voltage")
        current = self.get_data("current")
        # Naive example: find I where V is closest to 0
        idx = min(range(len(voltage)), key=lambda i: abs(voltage[i]))
        return {"units": "A", "data": current[idx]}

    def validate_observables(self, *observables) -> None:
        """Optional: sanity checks before plotting."""
        for obs in observables:
            if (
                obs not in self.data.get_allowed_observables()
                and obs not in self._processed_observables
            ):
                raise ValueError(f"Observable '{obs}' not available for IVProcessor")
```

This uses the `DataProcessorCore` machinery:

* raw requests are delegated to `data` by the DataProcessorCore,
* processed requests computed on demand and cached,
* units resolved consistently.

---

### Step 3 – Implement a `DeviceWorker` using `DeviceWorkerCore`

Now we glue everything together with an `IVDeviceWorker`.

It should:

* set the `data_type` and `processor_type`,
* define `plot_iv_curve` and `plot_iv_parameters`,
* use existing plotters.

```python
from contracts.device_worker import DeviceWorkerCore
from implementations.data.data_types.iv_data import IVData
from implementations.data.data_processors.iv_processor import IVProcessor
from implementations.plotters.scatter_plotter import ScatterPlotter  # hypothetical
from contracts.plotter_options import PlotterOptions  # or wherever it lives

class IVDeviceWorker(DeviceWorkerCore):
    def __init__(self, device, dataspec, plot_type, options: PlotterOptions):
        super().__init__(device, dataspec, plot_type, options)

        # Connect contracts
        self.set_data_type(IVData)
        self.set_processor_type(IVProcessor)

    def plot_iv_curve(self, title: str):
        """Plot V-I curve for all selected files."""
        plotter = ScatterPlotter(title=title)

        # self.data_processors is a dict: label → IVProcessor
        plotter.ready_plot(self.data_processors, self.options)
        plotter.draw_plot()

    def plot_iv_parameters(self, title: str):
        """Plot Voc and Isc as points or bars."""
        # You could reuse ScatterPlotter or something more tailored
        plotter = ScatterPlotter(title=title)

        # You might pre-process values into a form the plotter expects,
        # or let it call get_data("voc") / get_data("isc") directly.
        plotter.ready_plot(self.data_processors, self.options)
        plotter.draw_plot()
```

Notes:

* `DeviceWorkerCore.run()` will call the method referenced by `self.plot_type` (e.g. `"plot_iv_curve"`) and handle threading and signals.
* Each plot function **must instantiate its own plotter** to keep plotters stateless and reusable.

---

### Step 4 – Implement or reuse a `Plotter`

If you already have a generic `ScatterPlotter`, use it. A minimal custom plotter implementing the `Plotter` contract might look like:

```python
from contracts.plotter import Plotter
from contracts.plotter_options import PlotterOptions

import plotly.graph_objects as go

class ScatterPlotter(Plotter):
    def __init__(self, title: str):
        self.title = title
        self.fig = go.Figure()
        self.processors = None
        self.options = None

    def ready_plot(self, processors, options: PlotterOptions):
        # Store for later use
        self.processors = processors
        self.options = options

        self.fig.update_layout(title=self.title)

    def draw_plot(self):
        for label, processor in self.processors.items():
            x = processor.get_data("voltage")
            y = processor.get_data("current")
            self.fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    mode="lines+markers",
                    name=label,
                )
            )

        self.fig.update_xaxes(title=processor.get_units("voltage"))
        self.fig.update_yaxes(title=processor.get_units("current"))
        self.fig.show()
```

---

### Step 5 – Add a widget and `option_alias`es

For the IV device you might want:

* a checkbox for “log y-axis”
* a checkbox for “show markers”
* maybe a dropdown for which derived parameter to show in the parameters plot

In your Qt Designer / XML file, set:

* `option_alias="log_y"` on the log-scale checkbox
* `option_alias="show_markers"` on the markers checkbox

The GUI will read those, build a `PlotterOptions`:

```python
options.add_option("log_y", True or False)
options.add_option("show_markers", True or False)
```

Your plotter can then react:

```python
if options.get_option("log_y"):
    self.fig.update_yaxes(type="log")
```

`PlotterOptions` is just a small dict wrapper with helper methods, but it’s the key bridge between GUI choices and plotting logic.

---

## Recap

To implement a new workflow in the X-LAB framework, you:

1. **Define a `DataCore` subclass** to read files and expose raw observables.
2. **Define a `DataProcessorCore` subclass** to compute derived quantities needed for your science.
3. **Define a `DeviceWorkerCore` subclass** that sets types, exposes `plot_*` methods, and instantiates plotters.
4. **Reuse or implement `Plotter` subclasses** to convert processors into visualisations.
5. **Add a widget with `option_alias`es** so users can control plots via the GUI, flowing through `PlotterOptions`.

At every step, keep asking:

> **Can I reuse an existing reader, DataCore, processor, plotter, or widget?**

If the answer is “yes”, your implementation will stay small, robust, and easy for the next scientist to understand.
