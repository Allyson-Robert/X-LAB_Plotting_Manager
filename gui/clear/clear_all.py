from PyQt5 import QtWidgets
from gui.clear.clear_data import clear_data


def clear_all(window: QtWidgets.QMainWindow):
    """
    Fully reset the GUI state and remove all in-memory data.

    This helper:
    - Clears the active `DataSpec` and GUI fields via `clear_data`.
    - Empties the console widget.
    - Writes a confirmation message to the GUI console.

    Parameters
    ----------
    window : QMainWindow
        Main application window whose state should be cleared.
    """
    clear_data(window)
    window.consoleTextEdit.clear()
    window.console_print("Cleared memory")
