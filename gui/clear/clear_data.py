from PyQt5 import QtWidgets


def clear_data(window: QtWidgets.QMainWindow):
    # Reset fields and properties related to dataspec
    window.dataspec = None
    window.dataspec_location = None

    window.currSetNameLineEdit.clear()
    window.currDeviceLineEdit.clear()
    window.notesPlainText.clear()
    window.console_print("Cleared dataspec from memory")

    window.stackedWidget.setCurrentWidget(window.stackedWidget.widget(0))
    window.selectedFilesList.clear()
    window.plotTypeCombo.clear()
