from abc import ABC, abstractmethod


class ScatterCollection(ABC):
    @abstractmethod
    def read_data(self, collection):
        pass

    @abstractmethod
    def get_data(self):
        pass
