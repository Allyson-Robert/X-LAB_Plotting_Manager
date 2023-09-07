from abc import ABC, abstractmethod


# Abstract class for all data types
class Data(ABC):

    @abstractmethod
    def read_file(self, filepath: str) -> None:
        pass

    @abstractmethod
    def get_data(self, observable: str) -> list:
        pass

    @abstractmethod
    def get_units(self, observable: str) -> str:
        pass

    @abstractmethod
    def get_allowed_observables(self):
        pass


# Master class with implementation of 1) get_data, 2) get_units and 3) get_allowed_observables
class DataCore(Data):
    def __init__(self):
        self.raw_data = {}
        self._allowed_observables = {}

    @abstractmethod
    def read_file(self, filepath: str) -> None:
        pass

    def get_data(self, observable: str):
        if observable in self._allowed_observables:
            return self.raw_data[observable]['data']
        else:
            raise ValueError(f"{self.__class__.__name__} does not contain {observable} data")

    def get_units(self, observable: str) -> str:
        self.get_data(observable)
        return self.raw_data[observable]["units"]

    def get_allowed_observables(self):
        return self._allowed_observables
