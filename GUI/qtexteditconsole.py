import logging
from PyQt5 import QtCore, QtWidgets


class QTextEditConsole(logging.Handler, QtWidgets.QTextEdit):
    """
    Subclass of QTextEdit that can serve as a console for the GUI.
    This subclasses both QTextEdit and logging.Handler in order to be used with the logging module.
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
