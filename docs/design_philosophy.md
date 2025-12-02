# How to think about this application?


## Some general notes to consider

### Modular, Reusable Components with Single Responsibility
The goal of the X‑LAB plotting framework is to help you turn raw scientific measurements into meaningful, 
reusable visualisations with minimal effort. The most important philosophy behind the entire system is **reuse**. 
This application is best integrated in your workflow by remembering to approach it from a 
modular angle.
You should always ask yourself:

> **“Can I reuse something that already exists?”**

Because over time your lab will accumulate:
- reusable *readers*, 
- reusable *DataCore*, *DataProcessorCore* and *Plotter* subclasses,
- portable *DeviceWorkerCore* subclasses with their widgets

This reuse-first mindset ensures that even complex analyses remain understandable and maintainable.
It is also further enhanced by the concept of single responsibility, which is core to the structure 
defined by the contracts. 
Keep this single responsibility and modularity in mind when extending this application to suit your needs.

### Abstract Base Classes (ABCs) vs Core Implementations

The framework exposes four architectural building blocks:

- `Data`  
- `DataProcessor`  
- `DeviceWorker`  
- `Plotter`  

Each defines **what a new implementation must provide**.  
On top of these, the framework offers recommended **Core versions**:

- `DataCore`  
- `DataProcessorCore`  
- `DeviceWorkerCore`  

The Core versions implement conventions and mechanisms encouraging structure and single-responsibility programming.
You are free to implement the ABCs directly, but using the Core classes requires far less code as it provides a foundational interaction between the various components of this application.

### A Bidirectional Way of Thinking

Developing a new implementation is not a bottom‑up process. It is *bidirectional*:

- **Data → Observables → Processing → Derived quantities**  
- **Device → Visualisations → Plot functions → Plotters**

As a scientist, you will switch constantly between these two directions:

* What does my data contain? 
* What can I read from the file? 
* Which quantities can I derive from it?  

and

* What do I want to visualise?
* How do I want to visualise it?
* What must I access to show this?

This interplay is what shapes your implementation.

### You Already Have a Working Default Implementation

If you installed the default module, you should already be able to:

- create a dataset, pointing to two‑column files (e.g. voltage–current, time–signal, wavelength–intensity),  
- and plot those directly from the GUI.

This documentation helps you go beyond that—building your own scientific visualisation workflows.

---

## Building Your Own Implementation: A Scientist’s Workflow

This section walks through the thought patterns you should follow when designing new analysis tools in the X‑LAB framework. It mirrors the real reasoning process I typically use in the lab.

---

### Step 1 — Understand Your Data

Before coding anything, inspect your raw files, what do they look like?

- Are these columnar text files or maybe matrices encoding an image?
- Do they contain headers, timestamps or metadata?  
- Which quantities are present and are they labelled??  
- What units are used?

And most importantly: Can the raw file already be successfully loaded by an existing file reader?

**Examples**
- An IV curve: Voltage (V) vs Current (A)  
- Time‑dependent signal: Time (s) vs intensity  
- LBIC: a 2D grid of currents  
- Spectra: wavelength vs counts  
- Temperature measurements: timestamp vs sensor value  

---

### Step 2 — Map Raw Data to *Observables* Using a DataCore Subclass

Subclassing `DataCore` lets you define:

- which file reader is used to import the raw data  
- how observables map to the general/agnostic structure returned by the reader 
- what each observable’s units are  
- optional extraction of timestamps  
- storage of raw values in the standard observable dictionary structure

### Your Thought Process Might Look Like This:
- “This file has two columns → I can reuse the csv reader I already have.”  
- “Column 0 is voltage → observable `voltage`, units `V`.”  
- “Column 1 is current → observable `current`, units `A`.”  
- “I need the measurement timestamp → extract it from the filename or from the metadata.”  

This gives the processor a clean, structured interface.

---

### Step 3 — Decide What Derived Quantities You Need And Let DataProcessorCore Subclasses Compute them

Once raw observables exist, you think:

> **“What quantities do I need from this data? Is the raw data enough or can I compute any derived quantities”**

**Examples**
- IV: Aside from current-voltage curve one might want to know the open-circuit voltage, short-circuit current, fill factor, and maximum power point  
- Light-beam Induced Current scans give you axes and a current map, but you might want to extract a profile or look at the distribution of currents.
- Time‑dependent IV: power conversion over time  
- Spectra: peak wavelength, full width at half maximum, integrated intensity  

A `DataProcessorCore` subclass allows you to add processing functions:

```python
self._processing_functions = {
    "isc": self.compute_short_circuit_current,
    "voc": self.compute_open_circuit_voltage,
    "pce": self.compute_power_conversion_efficiency,
}
```

The processor:
- requests raw data from `Data` subclasses
- computes derived quantities when needed  
- returns them in the same structured observable format  
- caches results for efficiency  

Your scientific reasoning—“what do I want to calculate?”—maps directly onto this class.

---

### Step 4 — Think About the Visualisations You Want

This is where the *bidirectional* aspect of the implementation starts becoming important:

> **“Given the data and derived observables, what plots do I want to be able to produce?”**

One dataset → many plots.

**Examples**

**IV Device**
- Raw IV curve  
- Efficiency extracted parameters  
- Time dependent behaviour

**LBIC Device**
- Heatmap of current density  
- Histogram of pixel values  
- Profiles along x and y  

Each of these can be obtained from the same basic data files but must be handled differently, usually by a dedicated `DeviceWorker` and `DataProcessor`, to produce the desired visualisation.
Each `DeviceWorker` subclass is therefore coupled to a `DataProcessor` and `Data` class and plots becomes dedicated `plot_{name}` method inside your DeviceWorker subclass.
These names also populate the GUI’s “plot selector”, so choosing clear names helps users understand what each plot does.
---

### Step 5 — Build the DeviceWorker (The Orchestrator)

A DeviceWorker does four things:

1. Sets the `data_type` (your DataCore subclass) and `processor_type` (your Processor subclass) during initialisation 
2. Defines multiple **plot functions**, one for each plot type (named `plot_{name}` as these are automatically detected by the GUI)  
3. Instantiates the needed **Plotter** inside each plot function, passing options and processors to it as needed.

**Your Internal Monologue Might Be**:
- “This LBIC device should expose: image, histogram, and profile plots.”  
- “Each is a separate plot function.”  
- “Each plot function will instantiate the appropriate plotter.”  
- “The plotter only gets processors and options—it never reads files directly.”  

Workers never implement scientific logic and plotters should never need to know the desired observables.
It is the task of the `DeviceWorker` to tell the plotter which observables to request from the `DataProcessor`.
This ensures plotters stay reusable between devices and measurement types.
In short they connect data → processors → plotters.

Add the new worker class name to `implementations.devices.__init__.py`.

```
from . import workers

__all__ = [
    "Generic",
    "NewWorker
]
```

---

### Step 6 — Provide a Widget for User Options

Each device needs its own widget, these are searched for by the GUI.  
It serves as the user’s scientific control panel.

**Thought Process**
- “Should the user choose the axis?” → combo box with `option_alias="x_axis"`  
- “Should they toggle log‑scale?” → check box with `option_alias="log_y"`  
- “Do they need a threshold?” → spin box with `option_alias="threshold"`  

The GUI automatically gathers these into a `PlotterOptions` object and passes it to the worker, which hands it over to the plotter to read and use if appropriate.

This keeps plotters GUI‑independent.

You can build widgets using:
- Qt Designer (recommended)  
- A simple XML template you can copy and edit  

---

### Step 7 — Choose or Reuse a Plotter

Plotters turn processed data into visuals.  
They should be as dumb and reusable as possible.

Typical plotters include:
- ScatterPlotter  
- HeatmapPlotter  
- HistogramPlotter 

If your visualisation matches any of these → **reuse**.

Only create a new plotter when the visualisation is fundamentally different.
Note that `Plotters` don’t maintain state between plots, they are instantiated by the GUI and removed when the plot has been generated.

---

## Understanding the Dataset
These datasets are fundamental to the GUI and are the main reason everything is interoperable.
They can be created using the data creation window, are rebuilt when selecting files from any set to plot, and are used by all Cores to know where to find data.
But one might wonder what they are, in short they are small metadata files containing:

- labelled paths to raw measurement files,  
- optional colours or other needed metadata,  
- an experiment reference date,

**Raw data is never modified, overwritten, or copied.**  
It stays wherever *you* keep it—your folder structure, your naming scheme, your archive.

A dataset is just a **pointer + metadata**.  
It allows the worker to collect the correct files and instantiate a processor for each.

This separation makes your workflow repeatable and safe.
For more details see the [dataset page](datasets.md).

---

## Final Thoughts

### Use Core Classes When Possible

They:
- implement standard observable format  
- implement processing‑function patterns  
- implement multi‑file handling  
- implement worker threading  
- integrate cleanly with the GUI  

Using them means you only implement the parts that matter scientifically.

### Deviate Only When Necessary

If your data or workflow doesn’t fit the model:
- you can use the ABCs directly  
- but then **you** must ensure compatibility  
- plotters cannot assume Core behavior  
- you must follow observable formatting yourself  

This is an advanced path—only use it when the science requires it.


By following this workflow‑oriented design approach, your implementation will naturally fit the X‑LAB ecosystem:

- raw data → observables → derived quantities  
- datasets pointing to files + metadata  
- devices offering multiple scientific workflows  
- widgets capturing user intent  
- plotters turning processors into visualisations  

And throughout the entire process, remember:

> **Always reuse existing readers, processors, plotters, widgets, and devices whenever possible.**  
> **Subclass only when needed.**  
> **Implement the ABCs only when absolutely necessary.**

This is the mindset that keeps your code clean, scientific, powerful—and future‑proof.

