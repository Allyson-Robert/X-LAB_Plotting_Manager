X-Lab Plotting v2.0.0
===========================
Last update: **2023/03/10**

Plotting software written while pursuing a PhD at Hasselt University. 
This program can be used to create filesets and plot the contents of the files therein.

### Table of Contents
* ![Installation](#Installation)
* ![General Use](#General-Use)
* ![How to Expand](#How-to-Expand)
* ![Upcoming Features](#Upcoming-Features)


Installation
============

Dependencies
------------
| Data           | GUI            | Built-in |
|----------------|----------------|----------|
| Plotly v5.11.0 | PyQt5 v5.15.4  | datetime |
| Numpy v1.24.0  | natsort v8.2.0 | json     |
| Pandas v1.5.2  |                | csv      |
|                |                | sys      |
|                |                | os       |


General Use
===========
### Main window
![Main Window](./IMG/MainWindow.png)

### Menu bar
The menu bar contains three main submenu's: *"File"*, *"Plot Config"*, and *"Help"*

#### File
Most important is the *"File"* dropdown which allows the use to create, save and load filesets.
These filesets are json files containing some metadata about any particular analysis session as well as paths
to the files used in that session.

#### Plot Config
The *"Plot Config"* is currently under construction and is not yet functional.

#### Help
The *"Help"* links to a basic about window and to this documentation (not yet implemented).

### ExperimentDB creation
![Main Window](./IMG/DataCreationWindow.png)

ExperimentDB are created by opening the Data Creation Window by navigating the menu bar *"File -> Create Set"*.
Filesets must always be named and contain paths to datafiles.
Do not forget to select the correct Experiment Type at this step.
Adding datafiles can be done manually by browsing to the proper file and labelling each.
It is also possible to generate a set of datafiles automatically by navigating to the *"Automatic"* tab and choosing a directory.
Each file is then added and labelled with its name.
By default, the Data Creation Window is opened on the *"Manual"* tab.

Filesets are saved after creation and by navigating *"File -> Save Set"*. 
Do not forget to append the *".json"* file extension to the name when saving.

These filesets can also be loaded again by navigating *"File -> Load Set"*.
Note that only the fileset itself is loaded in this step.
The contents of each data file references in this fileset will only be loaded when plotting.

### Experiment
The experiment type is selected when a fileset is created and will alter some UI elements to reflect the type of 
analysis required for the device.
Any number of new experiments can be defined and included as needed by subclassing DeviceWorker and adding it to the GUI.
See ![here](#How-to-Expand) for more information
A number of experiments are included by default: Generic, Sunbrick, Stability, DW2000, LBIC, PDS, PTI.

### Notes
A text window is available to add notes to a fileset if necessary.
Any important remarks or findings can in this way remain associated with the files containing the data.

### Console
The program is moderately verbose and will offer warnings, errors and other runtime messages through the console at the bottom of the screen.
It can be useful to add the contents of the console to the fileset in order to save a particularly interesting sequence of plots.
This way plots can be easily reproduced manually by reading the console output.

Program Structure
=================
```mermaid
X-LAB Plot Manager
├── experimentdb
├── fileset
├── gui
│   ├── main
│   ├── data_creator
│   └── about.txt
├── plugins
│   ├── data
│   │   ├── data_processors
│   │   ├── data_types
│   ├── devices
│   └── plotter
```

How to Expand
=============
The structure of the software loosely follows the schema below.
The GUI calls an DeviceWorker class and initialises it with the required plot type, options and fileset.
This worker is passed to a separate thread where it can perform computations without freezing the GUI which is then free
to display progress.

The DeviceWorker must be aware of the type of data and dataprocessor to be used to initialise them.
Once the data is set (i.e. the processors are initialised and the data has been read from the files) the 
DeviceWorker will call an appropriate plotter depending on the specific plot type.
This plotter requires the processors and will retrieve data from them.

Cores are available for: DeviceWorker, DataProcessor and Data.
These contain default implementation that do not need to know much about the internals of the Data to function.
These Cores can be subclassed for quick/common additions.
If more control is required then subclass the abstract base classes directly.

```mermaid
classDiagram
GUI --> DeviceWorker: Calls
class DeviceWorker{
    DataProcessor processors
    set_data()
    set_options()
    set_data_type()
    set_processor_type()
    run()
    plot_*()
}
class Plotter{
    DataProcessor processors
    ready_plot()
    draw_plot()
}
class DataProcessor{
    Data data
    get_data()
    get_units()
    validate_observables()
    _compute_derived_observable()
}
class Data{
    data
    label
    read_file()
    get_data()
    get_units()
    get_allowed_observables()
}

DeviceWorker --> Data: Initialises
DeviceWorker --> Plotter: Calls
DeviceWorker --> DataProcessor: Initialises
Plotter --> DataProcessor: Calls
DataProcessor --> Data: Calls
```

### DeviceWorker
```mermaid
classDiagram
class DeviceWorker{
    DataProcessor processors
    set_data()
    set_options()
    set_data_type()
    set_processor_type()
    run()
}
<<Abstract>> DeviceWorker


class DeviceWorkerCore{
    set_data()
    set_data_type()
    set_processor_type()
    run()
}
```

### Plotter
```mermaid
classDiagram
class Plotter{
    DataProcessor processors
    ready_plot()
    draw_plot()
}
<<Abstract>> Plotter

```

### DataProcessor
```mermaid
classDiagram
class DataProcessor{
    Data data
    get_data()
    get_units()
    validate_observables()
    _compute_derived_observable()
}
<<Abstract>> DataProcessor

class DataProcessorCore{
    get_data()
    get_units()
    _compute_derived_observable()
}
```

### Data
```mermaid
classDiagram
class Data{
    data
    label
    read_file()
    get_data()
    get_units()
    get_allowed_observables()
}
<<Abstract>> Data

class DataCore{
    get_data()
    get_units()
    get_allowed_observables()
}
```

# Upcoming features
Here I will keep a list of features I need for the program to work well.

## Database storage
Currently, everything is recomputed every time when a dataset is loaded into the program.
Dataset functionality will be expanded to include the current json as well as SQL databases.
JSON datasets will keep functioning as they do now but database datasets will be able to save computed values for future use.

## HTML Autosave
The plots currently open in the browser, but sometimes you might need many plots for large datasets. 
An option will allow you to choose between drawing the plots in the browser or saving them to a local folder.

## ExperimentDB Creation redesign
The current implementation is rather clunky and independent of the type of data that is selected.
The automatic feature should be aware of the type of data it is aggregating in order to adjust how it works.
