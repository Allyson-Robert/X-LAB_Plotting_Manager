from abc import ABC, abstractmethod
from plugins.data.data_types.data import Data


class DataProcessor(ABC):
    @abstractmethod
    def get_data(self, observable: str):
        pass

    @abstractmethod
    def get_units(self, observable: str) -> str:
        pass

    @abstractmethod
    def validate_observables(self, *args) -> None:
        pass


class DataProcessorCore(DataProcessor):

    def __init__(self, data: Data):
        self.data = data
        self._processing_functions = {}
        self.processed_data = {}
        for key in self._processing_functions:
            self.processed_data[key] = None

        self._processed_observables = self.processed_data.keys()

    def get_data(self, observable: str, *args, **kwargs):
        # If observable is from raw data delegate to Data
        if observable in self.data.get_allowed_observables():
            return self.data.get_data(observable)

        # Compute processed data if needed
        elif observable in self._processed_observables:
            if self.processed_data[observable] is None:
                self.processed_data[observable] = self._processing_functions[observable]()
            return self.processed_data[observable]['data']
        else:
            raise ValueError(f"{self.__name__} does not contain {observable} data")

    def get_units(self, observable: str) -> str:
        self.get_data(observable)
        # Return raw data
        if observable in self.data.get_allowed_observables():
            return self.data.get_units(observable)
        elif observable in self._processed_observables:
            return self.processed_data[observable]["units"]
        else:
            raise ValueError(f"{self.__name__} does not contain {observable} data")

    @abstractmethod
    def validate_observables(self, *args) -> None:
        """
            This function will check whether all requested observables are available.
            This should be implemented by the individual subclasses
        """
        pass
