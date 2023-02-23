from abc import ABC, abstractmethod


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
