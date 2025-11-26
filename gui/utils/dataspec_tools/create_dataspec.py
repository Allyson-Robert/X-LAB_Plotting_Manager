from PyQt5 import QtWidgets
from utils.logging import with_logging
import gui.windows.DataSpecCreatorWindow
from gui.utils.clear.clear_data import clear_data
from gui.utils.dataspec_tools.load_dataspec import load_dataspec
from gui.utils.dataspec_tools.save_dataspec import save_dataspec

@with_logging
def create_dataspec(window: QtWidgets.QMainWindow, *args, **kwargs):
    """
    Launch the DataSpec creation dialog and construct a new dataspec from user input.

    Workflow:
    - Opens the DataSpec creator window populated with available devices.
    - On confirmation:
        * Clears existing state.
        * Stores the newly created dataspec.
        * Loads it into the GUI and updates the header.
        * Immediately saves it to disk.
    - If cancelled, informs the user that no dataspec was created.

    Parameters
    ----------
    window : QMainWindow
        Main application window controlling dataspec creation.
    """
    window.set_dataspec_window(gui.windows.DataSpecCreatorWindow.UiDataCreatorWindow(devices = [k for k in window.devices]))
    window.get_dataspec_window().show()

    if window.dataWindow.exec() == 1:
        # If the window was properly closed (Done button) then creation was successful
        #     Copy dataspec_tools and print to console
        clear_data(window)
        window.set_dataspec(window.get_dataspec_window().get_dataspec())
        window.console_print(f"DataSpec file created")
        load_dataspec(window)
        window.update_header()
        save_dataspec(window)
    else:
        # Warn user that window was improperly closed and that no dataspec_tools was created
        window.console_print("No DataSpec file was created")