from abc import ABC, abstractmethod
import os
from utils.custom_datetime import CustomDatetime
from contracts.observable import Observable
from contracts.file_readers import FileReaderFn
from typing import Any

# Abstract class_utils for all data types
class Data(ABC):
    """
    Abstract interface for data containers.

    Overview:
        Declares the contract for concrete data types used across the project.

    - Abstract methods: read_file, get_data, get_units, get_allowed_observables.
    - Intended as a minimal API that all data loaders/adapters must implement.

    Usage Notes:
        Implementations should populate an internal representation and match the return
        expectations used by callers elsewhere in the codebase.
    """

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


# Master class_utils with implementation of 1) get_data, 2) get_units and 3) get_allowed_observables
class DataCore(Data):
    """
        Base implementation providing common behaviors for data types.

        Overview:
            Supplies shared storage and partial method implementations useful to subclasses.

        - Manages `raw_data` and `_allowed_observables`.
        - Requires a `file_reader` conforming to `FileReaderFn` for loading raw data.
        - Implements datetime extraction from filenames, `get_data`, `get_units`,
          and `get_allowed_observables`.
        - Leaves `read_file` abstract so subclasses can:
            - call `self.file_reader(filepath)`
            - interpret its output into domain-specific observables.

        Usage Notes:
            Subclasses must implement `read_file` and populate `raw_data` / `_allowed_observables`.
            `get_data` raises ValueError for unsupported observables.
    """
    raw_data: dict[str, Observable]
    def __init__(self, file_reader: FileReaderFn):
        self.raw_data = {}
        self._allowed_observables = {}
        self.file_reader = file_reader

    @abstractmethod
    def read_file(self, filepath: str) -> None:
        pass

    def _get_datetime_from_filename(self, filepath: str) -> None:
        datetime = CustomDatetime()
        filename = os.path.basename(filepath)
        self.raw_data['datetime'] = {"units": None, "data": datetime.create_datetime_from_string(filename)}

    def get_data(self, observable: str) -> Any:
        if observable in self._allowed_observables:
            return self.raw_data[observable]['data']
        else:
            raise ValueError(f"{self.__class__.__name__} does not contain {observable} data")

    def get_units(self, observable: str) -> str:
        self.get_data(observable)
        return self.raw_data[observable]["units"]

    def get_allowed_observables(self):
        return self._allowed_observables
