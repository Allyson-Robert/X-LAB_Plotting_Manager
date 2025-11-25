from abc import ABC, abstractmethod
from contracts.data_types import Data
from contracts.observable import Observable
from typing import Callable


class DataProcessor(ABC):
    """
        Abstract interface for data processors that derive observables from raw Data.

        Overview:
            Defines the minimal contract for processing layers that expose
            computed observables and their units.

        - Abstract methods: get_data, get_units, validate_observables.
        - Focused on returning data and unit strings for named observables.

        Usage Notes:
            Implementations should delegate raw observables to a Data instance
            and compute derived observables on demand.
        """

    @abstractmethod
    def get_data(self, observable: str, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def get_units(self, observable: str, *args, **kwargs) -> str:
        pass

    @abstractmethod
    def validate_observables(self, *args, **kwargs) -> None:
        pass


class DataProcessorCore(DataProcessor):
    """
       Default on‑demand processing core for derived observables.

       Overview:
           Provides a processing-functions registry and a cache for computed results.
           Delegates raw observables to the wrapped Data object and computes others
           using registered functions.

       - Maintains `_processing_functions` and `processed_data` cache.
       - get_data/get_units compute lazily and raise ValueError if unknown.
       - validate_observables remains abstract for concrete checks.

       Usage Notes:
           Register per-observable processing functions in `_processing_functions`
           and ensure they return `{"units": str, "data": ...}`.
       """

    processed_data: dict[str, Observable]
    processing_functions: dict[str, Callable]

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
    def validate_observables(self, *args, **kwargs) -> None:
        """
            This function will check whether all requested observables are available.
            This should be implemented by the individual subclasses
        """
        pass

    def elapsed_time(self, *args, **kwargs) -> Observable:
        # Get a reference timestamp from *args
        reference_datetime = kwargs["experiment_datetime"]
        data_datetime = self.get_data("datetime")
        return {"units": "$Elapsed ~time ~(hrs)$", "data": data_datetime - reference_datetime}