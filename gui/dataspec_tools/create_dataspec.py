from PyQt5 import QtWidgets
import gui.windows.DataSpecCreatorWindow
from gui.clear.clear_data import clear_data
from gui.dataspec_tools.load_dataspec import load_dataspec
from gui.dataspec_tools.save_dataspec import save_dataspec


def create_dataspec(window: QtWidgets.QMainWindow):
    # Run the DataCreatorWindow
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