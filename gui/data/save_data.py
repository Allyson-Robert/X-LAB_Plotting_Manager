from PyQt5 import QtWidgets
import json
import dataspec_manager as fs


def save_data(window: QtWidgets.QMainWindow):
    # Make sure there is data to save
    if window.fileset is None:
        return window.console_print("Err: Must first load data", level="warning")

    # Run the file dialog
    file_name = QtWidgets.QFileDialog.getSaveFileName(window, "Save file to disk")[0]
    if file_name != "":
        # Dump the data into a json file and remember the location
        window.fileset_location = file_name
        with open(file_name, "w") as json_file:
            json.dump(window.fileset, json_file, cls=fs.DataSpecJSONEncoder)
        json_file.close()

        return window.console_print(f"Saved data to {file_name}")
    else:
        # File dialog was exited without choosing a file
        return window.console_print(f"No file selected")