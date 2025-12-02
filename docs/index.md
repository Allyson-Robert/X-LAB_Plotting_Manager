# X‑LAB Plotting Manager

The **X-LAB Plotting Manager** is a modular framework for turning raw scientific measurements into clean, reusable, publication-ready plots. It was created to address a common research problem: as experiments pile up, so do ad-hoc scripts, commented-out file lists, duplicated plotting code and “just tweak this one” workflows that quickly become unmaintainable and impossible to reproduce.

This framework offers a structured, scalable alternative.
By enforcing modular components with clear responsibilities and a configurable UI, it replaces tangled plotting scripts with a robust and reproducible analysis pipeline. It supports both quick exploratory work and long-term dataset management, making it a practical tool for anyone dealing with experimental data.

---

## What this framework provides

The system is built around **clear contracts** that define how devices, processors, and plotters behave.  
This yields maximum modularity and reusability.

At a high level, the framework consists of:

### • Dataset creation  
Define *what* to load, *how* to interpret it, and *which processor and plotter* to apply. 
Datasets are stored as JSON files that act as portable analysis definitions.

### • Analysis/Plotting execution  
The main window lets you loads a dataset (by creation or by reading from the disk), spawns worker threads, processes the data, and renders the plots.

### • Contract‑based extensibility  
You can implement new:

- `Data` types (for giving meaning to raw data)  
- `DataProcessor` classes (for computing derived quantities)  
- `Plotter` classes (for new visualisations)  
- `DeviceWorker` classes (for experiment‑specific orchestration)

Modules stay clean because each class only does *one thing*, and all pieces work together through stable interfaces.

### • Robust UI and threading  
Long operations (like reading hundreds of files) run in background threads so the UI stays responsive.

---

## Structure of these documentation pages

The documentation is organised to follow the natural workflow of using — and eventually extending — the framework. 
Each section builds on the previous one:
1. 
2. **Introduction (this page)**  
   Overview of the project, its motivation, and the philosophy behind the framework.

2. **Installation**  
   Instructions for installing the application, its dependencies, and a baseline `implementations` module.

3. **Getting Started**  
   A hands-on walkthrough showing how to load existing implementations and generate your first plot.

5. **How to think about this application?**
The architectural mindset: modularity, reuse, and the reasoning behind the framework’s design.

6. **How to implement the contracts?**  
Step-by-step guidance on creating your own `Data`, `DataProcessor`, `Plotter`, and `DeviceWorker` classes.

7. **What are datasets?**
Explanation of dataset files, their structure, how they define analyses, and why they enable reproducibility.

8. **Logging and debugging**
Tools and patterns for monitoring background workers, diagnosing issues, and keeping the UI stable.

9. **API Reference**
Class and module documentation for deeper integration or custom development.

The goal of this structure is to help you understand the framework quickly, use it effectively, and extend it confidently — giving you a robust foundation for clean, reproducible, and scalable scientific data analysis.

---