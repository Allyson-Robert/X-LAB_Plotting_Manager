from abc import ABC, abstractmethod


class ScatterDataProcessor(ABC):

    @abstractmethod
    def get_data(self, observable: str):
        pass
