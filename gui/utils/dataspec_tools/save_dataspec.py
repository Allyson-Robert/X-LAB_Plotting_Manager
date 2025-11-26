from PyQt5 import QtWidgets
import json
import dataspec_manager as fs
from utils.logging import with_logging

@with_logging
def save_dataspec(window: QtWidgets.QMainWindow, *args, **kwargs):
    """
    Save the currently loaded dataspec to disk using a file dialog.

    Behaviour:
    - Ensures a dataspec is loaded before saving.
    - Opens a save-file dialog and writes the dataspec via `DataSpecJSONEncoder`.
    - Auto-appends a valid extension if necessary.
    - Updates the stored dataspec location and logs status messages.

    Parameters
    ----------
    window : QMainWindow
        GUI window containing the active dataspec.
    """

    # Make sure there is a dataspec to save
    if window.get_dataspec_name() is None:
        return window.console_print("Err: Must first load dataspec", level="warning")

    # Run the file dialog
    # TODO: There's a bug in ubuntu 24 that has the filter reinitialised when navigating the path
    file_name = QtWidgets.QFileDialog.getSaveFileName(
        parent=window,
        caption="Save file to disk",
        filter="DataSpecs (*.json *.dataspec *.ds);;All (*)",
        initialFilter="DataSpecs (*.json *.dataspec *.ds)"
    )[0]

    if file_name != "":
        # Dump the dataspec_tools into a json file and remember the location
        # TODO: Dataspec should be aware of its location

        # Ensure the file name has a valid extension
        if file_name:
            if not any(file_name.endswith(ext) for ext in ('.json', '.dataspec', '.ds')):
                # Default to .dataspec if no valid extension
                file_name += '.ds'

        with open(file_name, "w") as json_file:
            current_dataspec = window.get_dataspec()
            json.dump(current_dataspec, json_file, cls=fs.DataSpecJSONEncoder)
            current_dataspec.set_location(file_name)
        json_file.close()

        return window.console_print(f"Saved dataspec file to {file_name}")
    else:
        # File dialog was exited without choosing a file
        return window.console_print(f"No file selected")