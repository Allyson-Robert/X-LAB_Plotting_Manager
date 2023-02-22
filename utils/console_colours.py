from PyQt5 import QtGui


class ConsoleColours:
    def __init__(self):
        self._alert = QtGui.QColor(255, 0, 0)
        self._warning = QtGui.QColor(255, 127, 0)
        self._normal = QtGui.QColor(255,255,255)

    def get_colour(self, level):
        return getattr(self, f"_{level}")
