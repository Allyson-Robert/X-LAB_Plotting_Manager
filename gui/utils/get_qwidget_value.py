from PyQt5 import QtWidgets


def _cast_none_string_to_none_type(string: str):
    assert isinstance(string, str)
    if string == "None" or string == "none":
        return None
    return string


def get_qwidget_value(widget):
    """
    Extract the current value from common Qt widget types.

    Supported widgets:
    - QDoubleSpinBox / QSpinBox → numeric value
    - QCheckBox → boolean `isChecked`
    - QLineEdit / QComboBox → text, with "None"/"none" mapped to `None`

    Raises `NotImplementedError` if the widget type is unsupported.

    Parameters
    ----------
    widget : QWidget
        The widget whose value should be extracted.

    Returns
    -------
    Any
        The widget's value in a Python-friendly type.
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
