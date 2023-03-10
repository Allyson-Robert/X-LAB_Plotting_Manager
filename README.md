X-Lab Plotting v2.0.0
===========================
Last update: **2023/03/10**

Plotting software written while pursuing a PhD at Hasselt University. 
This program can be used to create filesets and plot the contents of the files therein.
For installation information see the ![Installation](https://github.com/Allyson-Robert/Plotting_Tool/edit/master/README.md#installation) section.

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
![Main Window](./IMG/MainWindow.png)

### Main menu
The menu bar contains some limited functionality including the ability to close the program or show a basic *about* section.
More importantly is the *"Data"* dropdown which allows the use to create, save and load filesets.

### Filesets
![Main Window](./IMG/DataCreationWindow.png)

Fileset are python dictionaries saved as json files.
They are created by opening the Data Creation Window by navigating the menu bar *"Data -> Create"*.
Filesets must always be named and contain datafiles.
Do not forget to select the correct Device Type at this step.
Adding datafiles can be done manually by browsing to the proper file and labelling each.
It is also possible to generate a set of datafiles automatically by navigating to the *"Automatic"* tab and choosing a directory.
Each file is then added and labelled with its name.
By default the Data Creation Window is opened on the *"Manual"* tab.

Filesets are saved by navigating *"Data -> Save"*. 
Do not forget to append the *".json"* file extension to the name when saving.

These filesets can also be loaded again by navigating *"Data -> Load"*.
Note that only the fileset itself is loaded in this step.
The contents of each data file references in this fileset will only be loaded when plotting.

### Experiment
The experiment type is selected when a fileset is created and will alter some UI elements to reflect the type of analysis required for the device.
A short summary is provided for each device type below.
A number of experiments are included by default: Generic, Sunbrick, Stability, DW2000, LBIC, PDS, PTI.

### Notes
A text window is available to add notes to a fileset if necessary.
Any important remarks or findings can in this way remain associated with the files containing the data.

### Console
The program is moderately verbose and will offer warnings, errors and other runtime messages through the console at the bottom of the screen.
It can be useful to add the contents of the console to the fileset in order to save a particularly interesting sequence of plots.
This way plots can be easily reproduced manually by reading the console output.

How to Expand
=============
The structure of the software loosely follows the following schema.
```mermaid
graph TD;
    GUI --> ExperimentWorker;
    ExperimentWorker --> Data;
    ExperimentWorker --> Plotter;
    ExperimentWorker --> DataProcessor;
    Plotter --> DataProcessor;
    DataProcessor --> Data;
```
