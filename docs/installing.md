# Installing the Application

## 1) Install Python

Ensure you have **Python 3.10+** installed:  
https://www.python.org/downloads/

---

## 2) Clone the project

```bash
git clone https://github.com/Allyson-Robert/X-LAB_Plotting_Manager.git
```

---

## 3) Set up a virtual environment and install dependencies

```bash
cd X-LAB_Plotting_Manager

python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

# Example for Python 3.12
pip install -r requirements-312.txt
```

---

## 4) Add an implementation package

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

