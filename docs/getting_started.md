# Getting started

## Installation

```bash
pip install -r requirements.txt
```

## Implementation of contracts
To use this framework, you will need to implement the contracts defined in the `contracts` module.
Crucially, the following contracts must be implemented at least once in an `implementations` module:

 - **DeviceWorker | DeviceWorkerCore**: Starts in a thread and exposes available plot types for any given abstract 'device'. It is responsible for connecting Plotter, DataProcessor and Data components. 
 - **Data | DataCore**: Handles raw data access from files
 - **DataProcessor | DataProcessorCore**: Handles computation of any derived quantities from raw data, is the primary interface to obtain data for plotting. Defers to Data for raw data access.
 - **Plotter**: Handles plots and formatting, data is requested from DataProcessor

The `implementations` module must have the following structure:

```
implementations/
├── data/
│   ├── __init__.py
│   ├── data_processors/
│   │   └── __init__.py
│   └── data_types/
│       └── __init__.py
├── devices/
│   ├── widgets/
│   │   └── __init__.py
│   ├── workers/
│   │   └── __init__.py
│   └── __init__.py
├── plotters/
│   └── __init__.py
├── utils/
│   ├── constants.py
│   └── __init__.py
├── config.json
└── __init__.py
```


A basic example/starting point can be found in the following repository: [X-LAB Plotting Manager Implementations](https://github.com/Allyson-Robert/X-LAB_Plotting_Manager_Implementations)

## Running the GUI

```bash
python -m gui.windows.MainWindow
```
