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