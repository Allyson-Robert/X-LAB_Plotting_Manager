from abc import ABC, ABCMeta, abstractmethod
from fileset.fileset import Fileset
from PyQt5 import QtCore


class WorkerMeta(type(ABC), type(QtCore.QObject)):
    pass


class ExperimentWorker(ABC, QtCore.QObject, metaclass=WorkerMeta):
    @abstractmethod
    def set_data(self,  fileset: Fileset):
        pass

    @abstractmethod
    def run(self):
        pass


class ExperimentWorkerCore(ExperimentWorker):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(int)
    @abstractmethod
    def set_data(self, fileset: Fileset):
        pass

    def run(self):
        # Set the data
        self.set_data(self.fileset)

        # Grab the correct plot and execute it
        plot_type = getattr(self, self.plot_type)
        plot_type(title=self.fileset.get_name(), legend=self.legend)
        self.finished.emit()
