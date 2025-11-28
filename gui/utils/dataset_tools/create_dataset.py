from PyQt5 import QtWidgets
from utils.logging import with_logging
import gui.windows.DataSetCreatorWindow
from gui.utils.clear.clear_data import clear_data
from gui.utils.dataset_tools.load_dataset import load_dataset
from gui.utils.dataset_tools.save_dataset import save_dataset

@with_logging
def create_dataset(window: QtWidgets.QMainWindow, *args, **kwargs):
    """
    Launch the DataSet creation dialog and construct a new dataset from user input.

    Workflow:
    - Opens the DataSet creator window populated with available devices.
    - On confirmation:
        * Clears existing state.
        * Stores the newly created dataset.
        * Loads it into the GUI and updates the header.
        * Immediately saves it to disk.
    - If cancelled, informs the user that no dataset was created.

    Parameters
    ----------
    window : QMainWindow
        Main application window controlling dataset creation.
    """
    window.set_dataset_window(gui.windows.DataSetCreatorWindow.UiDataCreatorWindow(devices = [k for k in window.devices]))
    window.get_dataset_window().show()

    if window.dataWindow.exec() == 1:
        # If the window was properly closed (Done button) then creation was successful
        #     Copy dataset_tools and print to console
        clear_data(window)
        window.set_dataset(window.get_dataset_window().get_dataset())
        window.console_print(f"DataSet file created")
        load_dataset(window)
        window.update_header()
        save_dataset(window)
    else:
        # Warn user that window was improperly closed and that no dataset_tools was created
        window.console_print("No DataSet file was created")