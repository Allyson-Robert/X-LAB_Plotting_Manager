# Datasets

A **dataset** is a small, portable configuration file describing *which data belongs together*, *how it should be interpreted*, and *how it can be plotted*. 
Datasets are human-readable JSON files with extensions such as:

- `.ds`  
- `.dataset`  
- `.json`  

These files are the backbone of the framework’s reproducible analysis system.

---

## Why datasets matter

Typical ad-hoc analysis involves scattering paths, parameters, units, and processing logic across multiple scripts. 
Over time, this leads to:

- inconsistent metadata  
- accidental path mistakes  
- hard-to-reproduce results  
- difficulty sharing analyses across a team  

A **dataset** solves this by acting as a *single source of truth*. 
It encapsulates:

- experiment metadata  
- device type  
- datafile grouping  
- labels and colours  
- the experiment timestamp  
- notes and documentation  

The GUI and framework then build the correct:

- data readers  
- processors  
- plotters  

…automatically and consistently.

---

## Typical lifecycle of a dataset

### 1. **Creation**

Datasets are primarily created using the **Data Creation Window** in the GUI.  
This ensures correctness and prevents invalid or incomplete JSON.

In this window the user:

- names the dataset  
- selects the device  
- sets the **experiment date & time**  
- adds one or more datafiles and assigns labels  
- optionally assigns colours  
- writes notes or comments  
- saves the dataset JSON to disk  

All required metadata is enforced by the window.

---

### 2. **Storage**

A dataset is stored as a compact JSON configuration. 
Key fields include:

- dataset name  
- creation timestamp  
- experiment timestamp  
- device identifier  
- list of files and their labels  
- optional colours  
- notes  

A custom encoder and decoder handle the saving and loading of `DataSet` instances from JSON files on disk.

**Example (illustrative only):**

```json
{
    "location": null,
    "name": "Example Set",
    "creation_date": "2025.12.02_14.19.54",
    "experiment_date_time": "2023.03.30_13.19.54",
    "device": "Generic",
    "notes": "",
    "console": {},
    "structure_type": "flat",
    "filepaths": {
        "Example IV Curve": "path/to/IV_2023_03_30_13_17_28.txt"
    },
    "colours": {}
}
```

*(This example demonstrates the structure only. Do not use it directly.)*

---

### 3. **Execution**

Once a dataset is loaded in the main GUI:

1. **Its files are automatically listed**  
2. **The user selects a subset of files** to plot  
3. **The device determines which plots are valid**  
4. **Plot options appear immediately**  
5. **The run happens in a background worker thread**  
6. **The reader, processor, and plotter cooperate automatically**  
7. **The result is displayed to the user**

---

## TL;DR

Datasets provide a clean, structured, reproducible way to define:

- what the data is  
- where it lives  
- how it should be interpreted  
- which device and plots apply  
- how files relate to one another  
- metadata needed for processing  

Together with the Data Creation Window, datasets transform analysis workflows from scattered scripts into a **declarative, maintainable, and shareable system**.
