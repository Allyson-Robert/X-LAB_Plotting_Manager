import logging
from PyQt5 import QtCore, QtWidgets


class QTextEditConsole(logging.Handler, QtWidgets.QTextEdit):
    """
    QTextEdit-based logging console widget for the GUI.

    This class bridges the `logging` module with a Qt text widget by:
    - Subclassing both `logging.Handler` and `QTextEdit`.
    - Emitting formatted log messages through a dedicated Qt signal
      (`appendTextEdit`), which is connected to the widget's `append` slot.
    - Keeping the text area read-only so it behaves like a console.

    Typical usage
    -------------
    - Create an instance and add it as a handler to a `logging.Logger`.
    - Configure a formatter for the handler.
    - Logged messages will appear in the GUI with the configured format.

    Parameters
    ----------
    parent : QWidget
        Parent widget that will own this console.
    """
    appendTextEdit = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        logging.Handler.__init__(self)
        super(QtWidgets.QTextEdit, self).__init__(parent)

        self.setReadOnly(True)
        self.appendTextEdit.connect(self.append)

    def emit(self, record):
        msg = self.format(record)
        self.appendTextEdit.emit(msg)
