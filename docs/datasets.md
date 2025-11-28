# datasets

A **dataset** is a central configuration object in this framework. It describes *which data it refers to*, and *how that data should be processed and visualised*.  

datasets are saved as small, human-readable JSON files, typically with extensions such as:

- `.ds`
- `.dataset`
- `.json` (depending on preference or tooling)

These files act as **portable analysis definitions**.

---

## Why datasets matter

In many ad-hoc analysis workflows, users prepare a Python script containing:

- A bundle of paths pointing to raw data
- Hand-written code selecting processors or plotters
- Hard-coded parameters and metadata

This approach becomes fragile quickly:

- Paths get copied incorrectly  
- Important metadata is lost or scattered across scripts  
- Reuse across experiments becomes painful  
- Sharing analysis logic across a team becomes inconsistent  

**datasets solve this problem.**

Instead of writing one script per dataset, you describe the experiment or analysis **in a structured JSON file**. 
The framework then:

- Loads the dataset  
- Resolves the correct devices, processors, readers, and plotters  
- Executes the run in a fully defined and reproducible way  

This gives repeatable, clean, long-lived analyses—without rewriting code.

---

## Typical lifecycle of a dataset

### 1. **Creation**

datasets are usually created through the **Data Creation Window** in the GUI.

The window helps users:

- Label a set of datafiles
- Select a device type - defining the plots that are compatible
- Setting an experiment date and time
- Select data sources and label them
- Save to disk to a valid dataset JSON file for reuse

This UI is recommended because it ensures correctness and reduces manual JSON editing errors.

---

### 2. **Storage**

datasets are stored as JSON files using the framework’s custom encoder/decoder.  
They are lightweight, human-editable, and versionable (ideal for Git).

---

### 3. **Execution**

When a run begins:

1. The dataset is loaded
2. The framework reads its fields
3. A subset of the files can be selected for plotting
4. The plot manager will construct matching device, processors, and plotters in a separate thread to prevent ui-lockup
5. Loading is reported to the user via the UI progress bar
6. The analysis/plot executes as defined by the devive, plotter and processor implementations
7. Results are shown as defined by the user

Because datasets are declarative, execution is consistent and repeatable.

---

## TL;DR

datasets are a **powerful, central abstraction** in this framework.  
They describe “where to find data” and what can be done with it in a clean, structured way, enabling:

- Reproducibility  
- Reuse  
- Metadata-driven analysis  
- Clean separation between data and code  
- Easy sharing across users and teams  

Together with the Data Creation Window, datasets transform analysis workflows from scattered scripts into a **coherent, modern, configuration-driven system**.
