from abc import ABC, abstractmethod


class ScatterDataProcessor(ABC):
    @abstractmethod
    def get_data(self, observable: str):
        pass

    @abstractmethod
    def get_units(self, observable: str) -> str:
        pass

    @abstractmethod
    def validate_observables(self, *args) -> None:
        pass
