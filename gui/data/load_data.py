from PyQt5 import QtWidgets
from utils.errors.errors import IncompatibleDeviceTypeFound
from gui.clear.clear_data import clear_data
from utils.logging import with_logging
import json
import fileset as fs


def open_data_file(window: QtWidgets.QMainWindow):
    # Choose file
    file_name = QtWidgets.QFileDialog.getOpenFileName(window, "Open Files")[0]
    if file_name != '':
        # Reset data
        clear_data(window)
        window.consoleTextEdit.clear()

        # Open then load the json file, remember the location and update gui
        window.fileset_location = file_name
        with open(file_name) as json_file:
            window.fileset = json.load(json_file, cls=fs.FilesetJSONDecoder)
            window.console_print(f"Opened {file_name}")
        try:
            window.notesPlainText.setPlainText(window.fileset.get_notes())
            load_data(window)
            window.update_header()
        except IncompatibleDeviceTypeFound:
            clear_data(window)
    else:
        # File not chosen
        window.console_print(f"Err: No file loaded", level="warning")


@with_logging
def load_data(window: QtWidgets.QMainWindow):
    # Add all top level keys to the selection list of the gui
    for label in window.fileset.get_labels():
        window.selectedFilesList.addItem(label)

    # FEATURE REQUEST: Make this a setting
    # Select all items by default
    window.selectedFilesList.selectAll()

    # Edit combobox to show all available plot types
    try:
        for plot_type in window.plot_types[window.fileset.get_device()]:
            window.plotTypeCombo.addItem(plot_type)
    except KeyError:
        window.console_print(
            f"Incompatible device type [{window.fileset.get_device()}] found in {window.fileset.get_name()}, select another fileset or implement the device type. Fileset path: N/A")
        raise IncompatibleDeviceTypeFound

    window.console_print("ExperimentDB loaded")