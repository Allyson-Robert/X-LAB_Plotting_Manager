import os
import natsort
from datetime import datetime


class Fileset:
    """
    This class collects paths to files containing relevant data. The exact contents of the files does not matter as
    only the locations are relevant for this class.
    Paths can be added by construction in which case the structure type is said to be 'structured'. Paths can also be
    added manually one by one, in this case the structure type is 'flat'.
    Flat and structured construction cannot be mixed
    """
    _allowed_structure_types = ("flat", "structured")
    _accepted_extensions = ("xlsx", "xls", "csv", "txt")

    def __init__(self, creation_date: str, experiment_date_time: str):
        assert isinstance(creation_date, str)
        assert isinstance(experiment_date_time, str)

        self.name = ""
        self.creation_date = datetime.strptime(creation_date, "%Y.%m.%d_%H.%M.%S")
        self.experiment_date_time = datetime.strptime(experiment_date_time, "%Y.%m.%d_%H.%M.%S")
        self.device = ""
        self.notes = ""
        self.console = {}
        self.structure_type = None
        self.filepaths = {}

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        assert isinstance(name, str)
        self.name = name

    def get_creation_date(self) -> str:
        return self.creation_date

    def get_experiment_date(self) -> str:
        return self.experiment_date_time

    def get_device(self) -> str:
        return self.device

    def set_device(self, device: str):
        assert isinstance(device, str)
        self.device = device

    def get_structure_type(self) -> str:
        return self.structure_type

    def set_structure_type(self, desired_type: str):
        assert desired_type in self._allowed_structure_types
        if self.structure_type is None:
            self.structure_type = desired_type

    def add_notes(self, additional_notes: str):
        assert isinstance(additional_notes, str)
        self.notes += additional_notes

    # TODO: this is probably redundant
    def set_notes(self, notes_content: str):
        assert isinstance(notes_content, str)
        self.notes = notes_content

    def get_notes(self) -> str:
        return self.notes

    def add_console(self, datetime: str, additional_console: str):
        assert isinstance(datetime, str)
        assert isinstance(additional_console, str)
        self.console[datetime] = additional_console

    # TODO: This could also be redundant
    def set_console(self, console_content: dict):
        assert isinstance(console_content, dict)
        self.console = console_content

    def get_console(self) -> dict:
        return self.console

    # Path management
    def add_filepath(self, path: str, label: str):
        if self.get_structure_type() != 'structured':
            # Check for duplicate label
            if label in self.filepaths.keys():
                return "Duplicate label found in fileset"
            else:
                # Add the file to the dataset and update the GUI
                self.filepaths[label] = path
        else:
            return "Constructed structure cannot be appended manually"

        return ""

    def construct_structured_filepaths(self, root_dir: str) -> str:
        """
        Will generate a structured file set and add it to the current filepaths. This will seek all files and
            subdirectories of the giver root_dir and append all data files to the filepaths attribute. Note that
            root_dir should be an absolute path.
        """
        if self.get_structure_type() != "flat":
            errors = ""
            items = natsort.natsorted(os.listdir(root_dir))
            for item in items:
                if item in self.filepaths.keys():
                    errors += f"Ignored {item}: duplicate label \n"
                    continue

                # Create nested dict for subdirectories
                path = f"{root_dir}/{item}"
                if not os.path.isfile(path):
                    self.filepaths[item] = {}
                    for file in natsort.natsorted(os.listdir(path)):
                        # Only append to dataset if file is actually a file with an accepted extension
                        filepath = f"{path}/{file}"
                        is_path_valid, error_msg = self._check_valid_path(filepath)
                        if is_path_valid:
                            self.filepaths[item][file] = filepath
                        else:
                            errors += error_msg
        else:
            errors = "Flat fileset cannot use structured construction"

        return errors

    def get_filepath(self, label: str) -> str:
        return self.filepaths[label]

    def get_filepaths(self) -> dict:
        return self.filepaths

    def get_labels(self):
        return self.filepaths.keys()

    def set_filepaths(self, filepaths: dict):
        assert isinstance(filepaths, dict)
        self.filepaths = filepaths

    # Checks are needed before paths are added to the fileset
    def _check_valid_path(self, path: str):
        assert isinstance(path, str)
        # Check whether the path exists and points to a file
        if os.path.exists(path) and os.path.isfile(path):
            # Check if the file has the proper extension
            if path.endswith(self._accepted_extensions):
                return True, ""
            else:
                return False, f"Forbidden Extension: Ignored {path}\n"
        elif os.path.exists(path) and not os.path.isfile(path):
            return False, f"Not a File: Ignored {path}\n"
        else:
            return False, f"Filesystem Error: Ignored {path}\n"

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False
