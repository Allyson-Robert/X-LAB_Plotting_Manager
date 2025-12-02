from PyQt5 import QtWidgets
import json
import dataset_manager as fs
from utils.logging import with_logging

@with_logging
def save_dataset(window: QtWidgets.QMainWindow, *args, **kwargs):
    """
    Save the currently loaded dataset to disk using a file dialog.

    Behaviour:
    - Ensures a dataset is loaded before saving.
    - Opens a save-file dialog and writes the dataset via `DataSetJSONEncoder`.
    - Auto-appends a valid extension if necessary.
    - Updates the stored dataset location and logs status messages.

    Parameters
    ----------
    window : QMainWindow
        GUI window containing the active dataset.
    """

    # Make sure there is a dataset to save
    if window.get_dataset_name() is None:
        return window.console_print("Err: Must first load dataset", level="warning")

    # Run the file dialog
    # TODO: There's a bug in ubuntu 24 that has the filter reinitialised when navigating the path
    file_name = QtWidgets.QFileDialog.getSaveFileName(
        parent=window,
        caption="Save file to disk",
        filter="DataSets (*.json *.dataset *.ds);;All (*)",
        initialFilter="DataSets (*.json *.dataset *.ds)"
    )[0]

    if file_name != "":
        # Ensure the file name has a valid extension
        if file_name:
            if not any(file_name.endswith(ext) for ext in ('.json', '.dataset', '.ds')):
                # Default to .dataset if no valid extension
                file_name += '.ds'

        with open(file_name, "w") as json_file:
            current_dataset = window.get_dataset()
            json.dump(current_dataset, json_file, cls=fs.DataSetJSONEncoder)
            current_dataset.set_location(file_name)
        json_file.close()

        return window.console_print(f"Saved dataset file to {file_name}")
    else:
        # File dialog was exited without choosing a file
        return window.console_print(f"No file selected")