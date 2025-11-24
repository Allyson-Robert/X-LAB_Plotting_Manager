# X-LAB Plotting Manager – GUI

Welcome to the documentation for the **X-LAB Plotting Manager GUI**.  
This repository contains a Qt-based desktop application that loads compatible implementations, and provides a unified user interface for loading data and generating publication-ready plots.

For a practical, hands-on overview of installing and running the GUI, start with the project’s root **README.md**. 
This `index.md` focuses on how the GUI is structured, how it interacts with implementation packages, and where to find or add API-level documentation.

---

## What lives in this repository?

At a high level, the GUI repository provides:

- The **main application window** and supporting dialogs.
- The **contract definitions** that describe how analysis/plotting implementations must behave.
- A small set of **core utilities** shared by the GUI and implementations (e.g. option handling, datetime helpers).

Implementation-specific logic (for individual devices, data formats, and plot types) is kept out of this repository and lives in separate implementation packages, which plug into the contracts defined here.

For installation and repository layout details, see **README.md** in the project root.

---

## Reading the API documentation

The long-term goal is to provide API documentation for most public classes, functions and modules in this repository. 
Once generated (e.g. via MkDocs + mkdocstrings or a similar tool), you’ll find the API reference under the **API** section of the navigation sidebar.

Typical entry points include:

- **GUI entry point and windows**
  - Main application window
  - Dialogs for selecting devices, data sets, and plots
- **Contracts / core abstractions**
  - `Data` / `DataCore`: base classes for raw data containers
  - `DataProcessor` / `DataProcessorCore`: base classes for derived/processed observables
  - `Plotter` and concrete plotter classes (e.g. heatmaps, line plots)
  - `DeviceWorker` / `DeviceWorkerCore`: threaded workers that orchestrate data loading and plotting
  - `PlotterOptions`: a lightweight container for plot configuration options
- **Utilities**
  - Custom datetime helpers
  - Plot-prep helpers (axes, colorbars, export configuration)
  - Miscellaneous Qt / threading helpers

If you are extending the system, it is worth browsing the API docs for each of these core contracts so you understand what the GUI expects from your implementations.

---

## Contracts: how the GUI talks to implementations

A central design goal of the X-LAB Plotting Manager is to keep the GUI generic and various implementations reusable across experiments. 
This is achieved through a small set of **contracts**—abstract base classes and simple helper types that define how user-provided implementations must behave. 
The most important contracts are:

### Data & DataProcessor

- **`Data` / `DataCore`** define the interface for raw data containers:
  - `read_file(filepath: str)` loads a single file into the container.
  - `get_data(observable: str)` returns a list or array for the requested observable (e.g. `"x_axis"`, `"current"`).
  - `get_units(observable: str)` reports the units for that observable.
  - `get_allowed_observables()` exposes the available observable names.

- **`DataProcessor` / `DataProcessorCore`** define how to compute **derived** observables on top of a `Data` instance:
  - `get_data(observable: str, *args, **kwargs)` returns either raw or processed data.
  - `get_units(observable: str)` returns the corresponding units.
  - `validate_observables(*args)` can be used by implementations to sanity-check that all required inputs are present.

In your implementations you typically subclass both `DataCore` and `DataProcessorCore` to support a particular file format and set of observables.

### Plotter & PlotterOptions

- **`Plotter`** defines the minimal interface that any plotter must implement:
  - `ready_plot(processors, options)` takes a dict of `DataProcessor` instances and a `PlotterOptions` instance and configures the plot.
  - `draw_plot()` renders the plot (e.g. using Plotly, Matplotlib, etc.) and displays or exports it.

- **`PlotterOptions`** is a simple key–value store used to pass configuration into plotters:
  - `add_option(label, value)` registers an option.
  - `get_option(label)` retrieves an option if present.
  - `has_options(labels)` checks whether one or more options have been set.

Plotters should be written so that all user-facing configuration comes in through `PlotterOptions`, making them easy to reuse across devices and data sets.

### DeviceWorker and background execution

- **`DeviceWorker` / `DeviceWorkerCore`** wrap a device + data specification + plot type into a single threaded worker:
  - `set_data_type(data_type)` tells the worker which `Data` subclass to use.
  - `set_processor_type(processor_type)` tells the worker which `DataProcessor` subclass to use.
  - `set_data(dataspec)` reads all files declared in a `DataSpec` and creates one `DataProcessor` per file.
  - `run()` wires everything together, calls the selected plotter and emits Qt signals for progress and completion.

The GUI instantiates and configures a `DeviceWorkerCore` based on the user’s choices, then hands it off to a `QThread` so plots can be prepared without blocking the interface.

---

## Implementing your own contracts

When you want to support a new device, data format, or plot style, you interact with the GUI through a small set of contracts. 
This section describes both the **higher-level workflow** that matches how a researcher would typically approach a new experiment and the **mechanics** (what to subclass and which methods to implement).

---

### 1 From new device to working plots: a suggested workflow

This section is written from the perspective of a researcher who has a **new experiment or device** and wants to add it to their fork of the GUI + implementations.

#### Step 1 – Understand your data and plots before touching code

Before subclassing anything, take a step back and ask:

- **Is my device’s data format already covered?**
  - Are the files identical or nearly identical to an existing device?
  - Are the observable names and units the same (or trivially mappable)?
- **Are the derived quantities already implemented by an existing processor?**
  - Do I need the same “current vs voltage” curves, resistance calculations, averages, etc. as an existing experiment?
- **Which types of plots do I actually need?**
  - Is it just standard line plots, histograms, heatmaps, etc. that already exist?
  - Do I need something fundamentally new (e.g. a 3D surface plot, special contour plot, or a highly customized layout)?

The goal here is to **maximize reuse**:
- If your raw data and derived quantities match an existing device, you can often keep using the existing `DataCore` and `DataProcessorCore` implementations.
- If your plotting needs are covered by existing plotters, you can simply wire them up for your new device.

This keeps your implementation thin and easier to maintain.

#### Step 2 – Reuse whenever possible

With that understanding:

- If your **data format is identical**, configure your new device to reuse an existing `DataCore` subclass.
- If your **processing logic is identical**, reuse the existing `DataProcessorCore` subclass.
- If your **plots are standard**, reuse one of the existing `Plotter` implementations (e.g. line plots, heatmaps).

In many cases, all you need is:

- A new **device worker** to bundle the correct data/processor/plotter combinations.
- A new **.ui file** to provide device-specific controls and naming in the GUI.

#### Step 3 – Create or subclass `DeviceWorkerCore` for your device

Once reuse options are clear, you usually:

1. **Subclass `DeviceWorkerCore`** in your implementations repo.
2. In this subclass:
   - Point it to the `DataCore` and `DataProcessorCore` types you want to use (existing or new).
   - Define which plots are available for this device (e.g. “I–V curve”, “Temperature map”, “Time trace”).
3. **Implement plot functions**:
   - For each plot your device supports, write a method like `plot_iv_curve()`:
     - Construct or update a `PlotterOptions` object based on GUI selections.
     - Choose the appropriate `Plotter` (existing or new).
     - Trigger the plotting pipeline.
   - These methods will be wired to buttons or actions in your device’s UI panel, and will appear in the GUI as user-selectable options.

This gives your new device a clear “menu” of plots that the GUI can present.

#### Step 4 – Design the device UI with Qt Designer

Next, give your device a proper control panel:

1. Open **Qt Designer** and create a new `.ui` file for your device:
   - Add controls for:
     - File/dataset selection (if applicable).
     - Plot options (e.g. dropdowns for axes, checkboxes for logarithmic scale, etc.).
     - Buttons to trigger each plot (e.g. “Plot I–V”, “Plot map”).
2. In your `DeviceWorkerCore` subclass:
   - Load this `.ui` file.
   - Connect the UI elements to your internal logic:
     - When a button is clicked, call the corresponding `plot_*` method.
     - When an option changes, update `PlotterOptions` or internal state.

Now your new device appears in the GUI with its own tailored layout and controls.

#### Step 5 – Add new contracts only when you truly need them

If, after all this, you discover that you **cannot reuse** existing pieces, that’s the moment to introduce new contract implementations:

- **New data type**:
  - Implement a new `DataCore` subclass if your file format or observable structure is genuinely different.
- **New processor**:
  - Implement a new `DataProcessorCore` subclass if your derived quantities are unique or complex enough to deserve their own processor.
- **New plot type**:
  - Implement a new `Plotter` subclass if you need a fundamentally new kind of visualization
    (e.g. a 3D surface plot, specialized contour plot, or multi-panel figure that isn’t covered yet).

Each of these new classes stays **generic**: they shouldn’t hard-code your device name or GUI behaviour. Instead, they provide reusable logic that your `DeviceWorkerCore` and `.ui` file orchestrate for a particular experiment.

---

In short:

- **Think reuse first**: can you use existing data types, processors, and plotters?
- **Use `DeviceWorkerCore` + `.ui`** to give your new device a home in the GUI and define which plots it offers.
- **Introduce new `DataCore`, `DataProcessorCore`, or `Plotter` implementations** only when your experiment truly needs a new capability.

This keeps your fork maintainable while still giving you the flexibility to handle new experiments and devices cleanly.


---

### 2. Step-by-step: implementing each contract

This part assumes you already know what you want to add and just need the concrete steps.

#### Data: reading and exposing raw observables

1. **Subclass `DataCore`** from the GUI’s core data module.
2. **Implement file loading**:
   - Provide a `read_file(filepath: str)` method that parses a single file produced by your device/experiment.
   - Store the results in an internal structure (often a dict) that maps observable names to
     `{"units": str, "data": Any}`.
3. **Expose observables and units**:
   - Implement `get_data(observable: str)` to return the raw data for that observable.
   - Implement `get_units(observable: str)` to return the corresponding units string.
   - Make sure `get_allowed_observables()` lists all supported observables so the rest of the system can query them.

If your device uses the exact same file format and observables as an existing data type, you can usually **reuse that existing `DataCore` subclass** instead of creating a new one.

#### DataProcessor: computing derived quantities

1. **Subclass `DataProcessorCore`**.
2. **Wire up processing functions**:
   - Fill `_processing_functions` with callables for each derived observable you want to support.
   - Each processing function should accept whatever raw/derived observables it needs and return the processed data.
3. **Implement the public interface**:
   - `get_data(observable: str, *args, **kwargs)` should:
     - Return raw data directly for pass-through observables, or
     - Call into the relevant processing function for derived ones.
   - `get_units(observable: str)` should return the correct units, whether raw or derived.
4. **Validate inputs**:
   - Use `validate_observables(*observables)` (or a similar helper) to ensure required inputs exist, and raise clear errors if not.

Again, if your device’s derived quantities are identical to an existing experiment (e.g. the same “resistance vs temperature” logic), you can often **reuse or lightly subclass an existing `DataProcessorCore` implementation**.

#### Plotter & PlotterOptions: turning processed data into figures

1. **Subclass `Plotter`** if you need a **new type of plot** (e.g. 3D surface, special stacked plots).
2. **Implement the plotting lifecycle**:
   - `ready_plot(processors: dict, options: PlotterOptions)`:
     - Read the data you need from the provided processors.
     - Read configuration values (axis selection, limits, colormaps, etc.) from `PlotterOptions`.
     - Prepare all necessary internal state (e.g. arrays, meshes, figure objects).
   - `draw_plot()`:
     - Render the figure using your plotting backend (Matplotlib, Plotly, …).
     - Either display the figure or return it to the GUI for embedding.
3. **Use `PlotterOptions` consistently**:
   - `PlotterOptions.add_option(label, value)` to register configuration from the GUI.
   - `PlotterOptions.get_option(label)` and `PlotterOptions.has_options()` to query configuration in your plotter.
   - Keep your plotter as stateless as possible beyond what’s set in `ready_plot()`.

If your experiment needs only standard 2D plots that are already supported (e.g. line plots, heatmaps), you can often **reuse existing `Plotter` implementations** and just feed them the right processors and options.

#### DeviceWorkerCore & GUI integration: wiring it all together

1. **Subclass `DeviceWorkerCore`** when you need a dedicated “device profile” with its own list of plots and controls.
2. **Configure types and data flow**:
   - Provide methods or attributes that set:
     - The `DataCore` subclass to use for this device.
     - The `DataProcessorCore` subclass to use.
     - The available plot functions and their associated `Plotter` types.
   - Ensure that `set_data_type`, `set_processor_type`, and `set_data` (or their equivalents) are correctly wired.
3. **Implement plot functions that the GUI will expose**:
   - Add clearly named methods (e.g. `plot_iv_curve`, `plot_temperature_map`) that:
     - Prepare `PlotterOptions` from GUI inputs or defaults.
     - Select the appropriate `Plotter`.
     - Trigger the plotting pipeline (often via a common helper).
4. **Connect to a `.ui` file**:
   - Design a device-specific panel in Qt Designer for your options and controls.
   - Load that `.ui` file in your `DeviceWorkerCore` subclass.
   - Connect UI elements (combo boxes, checkboxes, buttons) to your plot functions and option setters.

The GUI will then discover and present your device, its controls, and its plots as part of the normal workflow.

---

## Relationship to the README

This `index.md` is meant as a **conceptual front page** for the documentation site. It describes what the GUI does, which contracts it exposes, and how implementations plug in.

For **practical usage**—installation, environment setup, running the application, and repository-level notes—please refer to the project’s **README.md**. When in doubt:

- Start with `README.md` to get the project running.
- Come back to `index.md` and the API docs when you want to understand or extend the internals.

---

## Where to go next

Once the documentation is fully populated, you will typically navigate in this order:

1. **README.md** – clone, install, run the GUI.
2. **Getting Started** – screenshots and a walkthrough of loading example data and creating a first plot.
3. **Contracts** – in-depth explanation of `Data`, `DataProcessor`, `Plotter`, `DeviceWorker`, and `PlotterOptions`.
4. **API Reference** – module-by-module, class-by-class documentation.
5. **Implementation Recipes** – concrete examples of adding a new device, data format, or plot style.

This structure is intended to make the GUI repository a stable, reusable core while keeping all device- and experiment-specific logic in separate, easy-to-swap implementation packages.
