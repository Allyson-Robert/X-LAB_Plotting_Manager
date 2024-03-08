from PyQt5 import QtWidgets
from gui.clear.clear_data import clear_data


def clear_all(window: QtWidgets.QMainWindow):
    # Reset complete gui
    clear_data(window)
    window.consoleTextEdit.clear()
    window.console_print("Cleared memory")
