# X-LAB Plotting Manager

This repository contains the **X-LAB Plotting Manager**, a PyQt-based desktop
application for managing scientific data sets and generating publication-ready
plots.

This application provides a general interface for plotting scientific data.
![X-LAB Plotting Manager Screenshot](docs/images/MainWindow.png)

A secondary window allows users to create new data sets based on predefined
"dataspecs" that define the required data structure and metadata.
![DataCreationWindow Screenshot](docs/images/DataCreationWindow.png)

The GUI is built on top of a small core of contracts and utilities and expects
device- and experiment-specific logic to live in a separate `implementations`
package.

The general overview of this architecture is illustrated in the following diagram:
![Contract Diagram](docs/images/Contracts.png)


👉 **Full documentation**

The full documentation is in the `docs/` folder and published via MkDocs
(GitHub Pages):

- Project overview: [docs/index.md](docs/index.md)
- Installation & usage: [docs/getting-started.md](docs/getting-started.md)
- Dataspec format: [docs/dataspecs.md](docs/dataspecs.md)

---

## Quick start

```bash
# create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# run the GUI
python -m gui.windows.MainWindow
