# Getting started

The **X-LAB Plotting Manager** is a PyQt-based desktop application for managing scientific data and generating publication-ready plots.  
It is designed around a clean separation between:

- **Core GUI + contracts** (this repository), and  
- **Device/experiment-specific implementations** (separate package you provide)

## 🚀 Quick Installation

### 1) Install Python

Ensure you have **Python 3.10+** installed:  
https://www.python.org/downloads/

---

### 2) Clone the project

```bash
git clone https://github.com/Allyson-Robert/X-LAB_Plotting_Manager.git
```

---

### 3) Set up a virtual environment and install dependencies

```bash
cd X-LAB_Plotting_Manager

python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

# Example for Python 3.12
pip install -r requirements-312.txt
```

---

### 4) Add an implementation package

The GUI **requires an implementation** of the device/data/processor/plotter contracts.  
You may:

- Provide **your own** implementation inside `implementations/`  
- Or clone the official example implementation:

```bash
git clone https://github.com/Allyson-Robert/X-LAB_Plotting_Manager_Implementations.git implementations/
pip install -r implementations/requirements-312.txt
```

Without an implementation, the application will exit with an error on startup.

> ✨ **Yes—you can write your own full implementation!**  
> The documentation explains how to implement devices, datasets, data classes, processors, and plotters.

---

### 5) Launch the GUI

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

## Implementation of contracts
To use this framework, you will need to implement the contracts defined in the `contracts` module.
Crucially, the following contracts must be implemented at least once in an `implementations` module:

 - **DeviceWorker | DeviceWorkerCore**: Starts in a thread and exposes available plot types for any given abstract 'device'. It is responsible for connecting Plotter, DataProcessor and Data components. 
 - **Data | DataCore**: Handles raw data access from files
 - **DataProcessor | DataProcessorCore**: Handles computation of any derived quantities from raw data, is the primary interface to obtain data for plotting. Defers to Data for raw data access.
 - **Plotter**: Handles plots and formatting, data is requested from DataProcessor

![Contract Architecture](images/Contracts.png)

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

Before running the GUI, ensure that you have an `implementations` module as described above.
Also ensure that the root directory of the project is in your `PYTHONPATH`.
To launch the GUI, run the following command from the root of the project:

```bash
python -m gui.windows.MainWindow
```


