from abc import ABC, abstractmethod


class ScatterData(ABC):

    @abstractmethod
    def read_file(self, filepath: str):
        pass

    @abstractmethod
    def get_data(self, observable: str) -> list:
        pass

    @abstractmethod
    def get_units(self, observable: str) -> str:
        pass

