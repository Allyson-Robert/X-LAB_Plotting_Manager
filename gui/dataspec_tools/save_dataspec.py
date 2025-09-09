from PyQt5 import QtWidgets
import json
import dataspec_manager as fs


def save_dataspec(window: QtWidgets.QMainWindow):
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
                file_name += '.dataspec'

        window.dataspec_location = file_name
        with open(file_name, "w") as json_file:
            json.dump(window.get_dataspec(), json_file, cls=fs.DataSpecJSONEncoder)
        json_file.close()

        return window.console_print(f"Saved dataspec file to {file_name}")
    else:
        # File dialog was exited without choosing a file
        return window.console_print(f"No file selected")