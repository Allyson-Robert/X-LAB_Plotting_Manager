from PyQt5 import QtWidgets
from utils.errors.errors import IncompatibleDeviceTypeFound
from gui.clear.clear_data import clear_data
from utils.logging import with_logging
import json
import os
import dataspec_manager


# TODO: BUGFIX: Assumed notes and console are attributes and knows what they look like, same with plotTypeCombo
def open_dataspec_file(window: QtWidgets.QMainWindow, file_name: str = None):
    # Choose file if not specified
    if file_name is None:
        file_name = QtWidgets.QFileDialog.getOpenFileName(
            parent=window,
            caption="Open Files",
            filter="DataSpecs (*.json *.dataspec *.ds);;All (*)",
            initialFilter="DataSpecs (*.json *.dataspec *.ds)"
        )[0]

    # Check for empty filename
    if file_name == '':
        window.console_print(f"Err: No file specified", level="warning")
    else:
        # Reset dataspec_tools
        clear_data(window)
        window.consoleTextEdit.clear()

        # Open then load the json file, remember the location and update gui
        # window.fileset_location = file_name
        with open(file_name) as json_file:
            window.set_dataspec(json.load(json_file, cls=dataspec_manager.DataSpecJSONDecoder))
            window.console_print(f"Opened {file_name}")
        try:
            window.notesPlainText.setPlainText(window.dataspec.get_notes())
            load_dataspec(window)
            window.update_header()

        # Clear the dataspec_tools if loading failed
        except IncompatibleDeviceTypeFound:
            clear_data(window)
            window.console_print(f"Err: Loading failed", level="warning")


@with_logging
def load_dataspec(window: QtWidgets.QMainWindow):
    # Add all top level keys to the selection list of the gui
    for label in window.dataspec.get_labels():
        window.selectedFilesList.addItem(label)

    # FEATURE REQUEST: Make this a setting
    # Select all items by default
    window.selectedFilesList.selectAll()

    # Edit combobox to show all available plot types
    try:
        for function in window.get_plot_functions(window.get_current_device()):
            window.plotTypeCombo.addItem(function)

    except KeyError:
        window.console_print(
            f"Incompatible device type [{window.get_current_device()}] found in {window.get_dataspec_name()}, select another dataspec or implement the device type. DataSpec path: N/A")
        raise IncompatibleDeviceTypeFound

    window.console_print("DataSpec loaded")
