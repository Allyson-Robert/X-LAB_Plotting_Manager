from PyQt5 import QtWidgets

def search_for_first_active_radio_button(dialog: QtWidgets.QDialog) -> QtWidgets.QRadioButton:
    """
    Find and return the checked QRadioButton within a dialog.

    Scans all child radio buttons and returns the first active one.

    Parameters
    ----------
    dialog : QDialog
        Container widget containing radio buttons.

    Returns
    -------
    QRadioButton or None
        The checked radio button, or `None` if no selection exists.
    """
    for radio_button in dialog.findChildren(QtWidgets.QRadioButton):
        if radio_button.isChecked():
            return radio_button
    return None


