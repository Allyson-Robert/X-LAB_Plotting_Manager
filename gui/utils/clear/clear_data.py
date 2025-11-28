from PyQt5 import QtWidgets


def clear_data(window: QtWidgets.QMainWindow):
    """
    Clear the currently loaded dataset and reset all GUI widgets tied to it.

    Resets:
    - Stored `DataSet` object and its disk location.
    - Set name, device name, notes, and list widgets.
    - Plot type combobox and stacked widget view.

    A console message is printed to confirm completion.

    Parameters
    ----------
    window : QMainWindow
        Main GUI instance that holds dataset-related widgets.
    """
    window.dataset = None
    window.dataset_location = None

    window.currSetNameLineEdit.clear()
    window.currDeviceLineEdit.clear()
    window.notesPlainText.clear()
    window.console_print("Cleared dataset from memory")

    window.stackedWidget.setCurrentWidget(window.stackedWidget.widget(0))
    window.selectedFilesList.clear()
    window.plotTypeCombo.clear()
