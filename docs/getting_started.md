# Getting started

The **X-LAB Plotting Manager** is a PyQt-based desktop application for managing scientific data and generating publication-ready plots.  
It is designed around a clean separation between:

- **Core GUI + contracts** (this repository), and  
- **Device/experiment-specific implementations** (separate package you provide)

## Install the software
For instructions on installation see the [installation page](installing.md).

> ✨ Make sure that you have an *implementations* module ready before proceeding.
> This can be done by [writing your own](design_philosophy.md) or by cloning the provided [implementation](https://github.com/Allyson-Robert/X-LAB_Plotting_Manager_Implementations.git).

## 🚀 Launch the GUI

You can launch the GUI from your favourite IDE by pointing to `gui.windows.MainWindow` or by running the following command from the terminal:
```bash
python -m gui.windows.MainWindow
```

This opens the main application window:

![MainWindow](images/MainWindow.png)

---

## 📦 Creating a Dataset

From the menu bar:

**File → Create Set**

This opens the **Data Creation Window**, where you build datasets based on structured **datasets** that define required data inputs and metadata.

![DataCreationWindow](images/DataCreationWindow.png)

---

## 📉 Generating a plot

Once you have created a **DataSet**, it will appear in the main window with
a list of the available data, the device information is already loaded.
From here, generating a plot is quick and interactive.

------------------------------------------------------------------------

### 1️⃣ Select the Files You Want to Plot

The application is already aware of
- the available plot types for the device associated with the set
- the associated **Data** and **DataProcessor** types (from the implementations module)
- all **device-specific options** on the right are loaded from the correct widget

Inside the **Set Contents panel**, tick the files you want to include.
You can select:

-   a single file (e.g., one heatmap, one IV curve), or\
-   multiple files (for overlays, comparisons, etc.), depending on your
    device's capabilities.

This compatibility logic comes directly from how your device's
`DeviceWorker` and `Plotter` implementations declare supported plots.


------------------------------------------------------------------------

### 2️⃣ Adjust Plot Options

The **Options panel** on the right shows all customizable parameters for
the chosen plot.
This panel is defined by the widget for each device, meaning your implementation decides
what appears here.

Common options include:

-   z-ranges, profiles
-   normalisation
-   etc.

Two options are always available:
-   legend title
-   presentation

I use the latter to format my plots to be clearer in a presentation context where I want line traces to be thicker for example.
These options are gathered automatically into a `PlotterOptions` object:
Plotters retrieve these values using:

``` python
options.get_option("legend_title")
```

For example, a heatmap plotter can use these options to configure colour scales, ranges, and layout.

------------------------------------------------------------------------

### 3️⃣ Choose a Plot Type

Open the **Plot Type** dropdown.

Examples:
-   A 2D scan might enable **plot_image** and **plot_distribution**
-   A time-varying measurement might enable **plot**
-   IV measurements might enable **plot_forward** or **plot_forward_and_reverse**

Internally, the selected plot corresponds to a method defined inside
your device's worker.
This makes the system extensible: any worker method named `plot_*` can become a
selectable plot.

------------------------------------------------------------------------

### 4️⃣ Click **Plot**

Press the **Plot** button to start a worker and generate the visualisation.

Behind the scenes, the GUI:

1.  **Instantiates the device's worker**
2.  Sends it:
    -   a rebuilt DataSet containing the selected files
    -   the plot type
    -   a PlotterOptions instance
3.  Moves the worker into a background `QThread`
4.  Begins file reading (shown in the progress bar) and processing

Each selected file is read using your concrete `Data` subclass and associated file reader (`self.file_reader()`) and processed with your `DataProcessor` subclass (`get_data()`, derived observables, validation).

A progress bar updates live, and the plot is drawn once the worker emits
its `finished` signal.

------------------------------------------------------------------------

### 5️⃣ Enjoy Your Plot

Depending on your plotter implementation:

-   Plotly figures may open interactively (zoom, hover, export)\
-   Static plots can be saved as SVG/PNG/PDF\
-   Additional export helpers may run automatically

------------------------------------------------------------------------
