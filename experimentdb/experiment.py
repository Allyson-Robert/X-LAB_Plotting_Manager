import os
import natsort
from datetime import datetime
from experimentdb.measurement import Measurement


class Fileset:
    """
    This class collects paths to files containing relevant data. The exact contents of the files does not matter as
    only the locations are relevant for this class.
    Paths can be added by construction in which case the structure type is said to be 'structured'. Paths can also be
    added manually one by one, in this case the structure type is 'flat'.
    Flat and structured construction cannot be mixed
    """
    _accepted_extensions = ("xlsx", "xls", "csv", "txt")

    def __init__(self, creation_date: str):
        assert isinstance(creation_date, str)

        self.name = ""
        self.creation_date = datetime.strptime(creation_date, "%Y.%m.%d_%H.%M.%S")
        self.experiment_date_time = None
        self.device = ""
        self.notes = ""
        self.console = {}
        self.measurements = {}

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        assert isinstance(name, str)
        self.name = name

    def get_creation_date(self) -> datetime:
        return self.creation_date

    def set_experiment_date(self, experiment_date_time: str):
        assert isinstance(experiment_date_time, str)
        self.experiment_date_time = datetime.strptime(experiment_date_time, "%Y.%m.%d_%H.%M.%S")

    def get_experiment_date(self) -> datetime:
        return self.experiment_date_time

    def get_device(self) -> str:
        return self.device

    def set_device(self, device: str):
        assert isinstance(device, str)
        self.device = device

    def add_notes(self, additional_notes: str):
        assert isinstance(additional_notes, str)
        self.notes += additional_notes

    # CHECK: this is probably redundant
    def set_notes(self, notes_content: str):
        assert isinstance(notes_content, str)
        self.notes = notes_content

    def get_notes(self) -> str:
        return self.notes

    def add_console(self, date_and_time: str, additional_console: str):
        assert isinstance(date_and_time, str)
        assert isinstance(additional_console, str)
        self.console[date_and_time] = additional_console

    # CHECK: This could also be redundant
    def set_console(self, console_content: dict):
        assert isinstance(console_content, dict)
        self.console = console_content

    def get_console(self) -> dict:
        return self.console

    def add_measurement(self, path: str, label: str):
        # Checks for duplicate label
        if label in self.get_labels():
            raise ValueError(f"Measurement with this label ({label}) already exists")
        else:
            # Add the file to the dataset and update the GUI
            self.measurements = Measurement(path, label)

    def set_all_measurements(self):
        pass

    def get_measurements(self):
        pass

    def get_labels(self):
        return [measurement.get_label() for measurement in self.measurements]

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False
