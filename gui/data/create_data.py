from PyQt5 import QtWidgets
import gui.windows.DataCreatorWindow
from gui.clear.clear_data import clear_data
from gui.data.load_data import load_data
from gui.data.save_data import save_data


def create_data(window: QtWidgets.QMainWindow):
    # Run the DataCreatorWindow
    window.dataWindow = gui.windows.DataCreatorWindow.UiDataCreatorWindow(devices = [k for k in window.devices])
    window.dataWindow.show()

    if window.dataWindow.exec() == 1:
        # If the window was properly closed (Done button) then creation was successful
        #     Copy data and print to console
        clear_data(window)
        window.fileset = window.dataWindow.fileset
        window.console_print(f"ExperimentDB created")
        load_data(window)
        window.update_header()
        save_data(window)
    else:
        # Warn user that window was improperly closed and that no data was created
        window.console_print("No data was created")