from PyQt5 import QtWidgets


def _cast_none_string_to_none_type(string: str):
    assert isinstance(string, str)
    if string == "None" or string == "none":
        return None
    return string


def get_qwidget_value(widget):
    """
        Fetches the value of any the following QWidget types: QSpinbox, QCheckBox, QLineEdit
    """
    assert isinstance(widget, QtWidgets.QWidget)

    if isinstance(widget, QtWidgets.QDoubleSpinBox) or isinstance(widget, QtWidgets.QSpinBox):
        return widget.value()
    elif isinstance(widget, QtWidgets.QCheckBox):
        return widget.isChecked()
    elif isinstance(widget, QtWidgets.QLineEdit):
        return _cast_none_string_to_none_type(widget.text())
    elif isinstance(widget, QtWidgets.QComboBox):
        return _cast_none_string_to_none_type(widget.currentText())
    else:
        raise NotImplementedError
