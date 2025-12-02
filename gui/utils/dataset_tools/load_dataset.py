from PyQt5 import QtWidgets
from utils.errors.errors import IncompatibleDeviceTypeFound
from gui.utils.clear.clear_data import clear_data
from utils.logging import with_logging
import json
import dataset_manager


# TODO: BUGFIX: Assumed notes and console are attributes and knows what they look like, same with plotTypeCombo
@with_logging
def open_dataset_file(window: QtWidgets.QMainWindow, *args, **kwargs):
    """
    Open a dataset JSON file, load it into memory, and refresh the GUI.

    Behaviour:
    - Prompts the user for a file.
    - Clears existing dataset state.
    - Loads the JSON file using `DataSetJSONDecoder`.
    - Updates notes, file list, plot options, and header display.

    If loading fails due to an incompatible device type, the GUI is reset and a
    warning is printed.

    Parameters
    ----------
    window : QMainWindow
        GUI wrapper holding the active dataset.
    file_name : str, optional
        JSON file path. If omitted, a file dialog is opened.
    """
    # Choose file
    file_name = QtWidgets.QFileDialog.getOpenFileName(
        parent=window,
        caption="Open Files",
        filter="DataSets (*.json *.dataset *.ds);;All (*)",
        initialFilter="DataSets (*.json *.dataset *.ds)"
    )[0]

    # Check for empty filename
    if file_name == '':
        window.console_print(f"Err: No file specified", level="warning")
    else:
        # Reset dataset_tools
        clear_data(window)
        window.consoleTextEdit.clear()

        # Open then load the json file, and update gui
        with open(file_name) as json_file:
            dataset = json.load(json_file, cls=dataset_manager.DataSetJSONDecoder)
            dataset.set_location(file_name)
            window.set_dataset(dataset)
            window.console_print(f"Opened {file_name}")
        try:
            window.notesPlainText.setPlainText(window.dataset.get_notes())
            load_dataset(window)
            window.update_header()

        # Clear the dataset_tools if loading failed
        except IncompatibleDeviceTypeFound:
            clear_data(window)
            window.console_print(f"Err: Loading failed", level="warning")


@with_logging
def load_dataset(window: QtWidgets.QMainWindow):
    """
    Populate the GUI with data from the currently loaded dataset.

    Actions:
    - Adds all dataset labels to the file selection list.
    - Selects all items by default.
    - Populates the plot-type combobox with device-appropriate plotting functions.

    Raises
    ------
    IncompatibleDeviceTypeFound
        If the dataset’s device type does not match available plot handlers.

    Parameters
    ----------
    window : QMainWindow
        GUI instance holding a loaded dataset.
    """
    # Add all top level keys to the selection list of the gui
    for label in window.dataset.get_labels():
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
            f"Incompatible device type [{window.get_current_device()}] found in {window.get_dataset_name()}, select another dataset or implement the device type. DataSet path: N/A")
        raise IncompatibleDeviceTypeFound

    window.console_print("DataSet loaded")
