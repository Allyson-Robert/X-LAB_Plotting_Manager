from PyQt5 import QtWidgets

def search_for_active_radio_button(dialog: QtWidgets.QDialog) -> QtWidgets.QRadioButton:
    for radio_button in dialog.findChildren(QtWidgets.QRadioButton):
        if radio_button.isChecked():
            return radio_button
    return None


