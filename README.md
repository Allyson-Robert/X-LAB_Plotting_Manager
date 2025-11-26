# X-LAB Plotting Manager

This repository contains the **X-LAB Plotting Manager**, a PyQt-based desktop
application for managing scientific data sets and generating publication-ready
plots.

The GUI is built on top of a small core of contracts and utilities and expects
device- and experiment-specific logic to live in a separate `implementations`
package.

👉 **Full documentation**

The full documentation is in the `docs/` folder and published via MkDocs
(GitHub Pages):

- Project overview: [docs/index.md](docs/index.md)
- Installation & usage: [docs/getting-started.md](docs/getting-started.md)
- Architecture details: [docs/architecture.md](docs/architecture.md)
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
