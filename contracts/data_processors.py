from abc import ABC, abstractmethod
from contracts.data_types import Data


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
    """
    Default implementation enables calling observables by name. Processing functions should be declared and implemented
    for each desired derived observable.
    A processing function should only be responsible for its own observable by returning a dict with two items, the unit
    and the data itself {"units": str, "data": Any | list}.

    self.get_data will compute the observable just in time, returns the results and keeps them in self.processed_data
    self.get_units does the same but returns the "units" value rather than the "data" value.
    """

    def __init__(self, data: Data):
        self.data = data
        self._processing_functions = {
            "elapsed_time": self.elapsed_time
        }
        self.processed_data = {}
        for key in self._processing_functions:
            self.processed_data[key] = None

        self._processed_observables = self.processed_data.keys()

    def get_data(self, observable: str, *args, **kwargs):
        # If observable is available from raw data delegate to Data
        if observable in self.data.get_allowed_observables():
            return self.data.get_data(observable)

        # Compute processed data if needed
        elif observable in self._processed_observables:
            if self.processed_data[observable] is None:
                # Adds the data to the processed_data dict after computing it
                self.processed_data[observable] = self._processing_functions[observable](*args, **kwargs)

            # Simply return if already set
            return self.processed_data[observable]['data']
        else:
            # FIXME: Apparently object has no attribute '__name__'. Did you mean: '__ne__'? gets triggered when ValueError is raised
            raise ValueError(f"{self.__class__.__name__} does not contain {observable} data")

    def get_units(self, observable: str) -> str:
        self.get_data(observable)
        # Return raw data
        if observable in self.data.get_allowed_observables():
            return self.data.get_units(observable)
        elif observable in self._processed_observables:
            return self.processed_data[observable]["units"]
        else:
            raise ValueError(f"{self.__class__.__name__} does not contain {observable} data")

    @abstractmethod
    def validate_observables(self, *args) -> None:
        """
            This function will check whether all requested observables are available.
            This should be implemented by the individual subclasses
        """
        pass

    def elapsed_time(self, *args, **kwargs):
        # Get a reference timestamp from *args
        reference_datetime = kwargs["experiment_datetime"]
        data_datetime = self.get_data("datetime")
        return {"units": "$Elapsed ~time ~(hrs)$", "data": data_datetime - reference_datetime}