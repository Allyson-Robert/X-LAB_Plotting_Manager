from abc import ABC, abstractmethod


class ScatterDataProcessor(ABC):
    _processing_functions: dict

    @abstractmethod
    def get_data(self, observable: str):
        pass

    @abstractmethod
    def get_units(self, observable: str) -> str:
        pass
