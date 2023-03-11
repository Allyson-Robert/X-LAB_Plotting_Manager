from PyQt5 import QtWidgets


def get_qwidget_value(widget):
    """
        Fetches the value of any the following QWidget types: QSpinbox, QCheckBox, QLineEdit
    """
    assert isinstance(widget, QtWidgets.QWidget)

    if isinstance(widget, QtWidgets.QSpinBox):
        return widget.value()
    elif isinstance(widget, QtWidgets.QDoubleSpinBox):
        return widget.value()
    elif isinstance(widget, QtWidgets.QCheckBox):
        return widget.isChecked()
    elif isinstance(widget, QtWidgets.QLineEdit):
        return widget.text()
    else:
        raise NotImplementedError
