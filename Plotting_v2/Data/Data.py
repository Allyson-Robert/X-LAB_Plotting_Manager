from abc import ABC, abstractmethod


class Data(ABC):
    @abstractmethod
    def get_label(self):
        pass

    @abstractmethod
    def get_data(self, observable):
        pass

    @classmethod
    def read_from_file(cls, filename):
        pass