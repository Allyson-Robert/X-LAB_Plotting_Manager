from abc import ABC, abstractmethod
from fileset.fileset import Fileset


class Experiment(ABC):
    @abstractmethod
    def set_data(self,  fileset: Fileset):
        pass

