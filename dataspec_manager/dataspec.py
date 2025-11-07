import os
from pathlib import Path
import natsort
from datetime import datetime
import warnings


class DataSpec:
    """
    This class collects paths to files containing relevant dataspec. The exact contents of the files does not matter as
    only the locations are relevant for this class. DataSpecs can currently contain straight up files ('flat') or
    directories containing files ('grouped_by_dir').
    The former can be added manually one at a time, the latter must be automatically constructed. Both types cannot be
    mixed.
    """
    # TODO: properly deprecate structured, assume flat for now
    _allowed_structure_types = ("flat", "dirlabelled", "structured")
    _accepted_extensions = ("xlsx", "xls", "csv", "txt", "dpt", "json")

    def __init__(self, creation_date: str):
        assert isinstance(creation_date, str)
        # FEATURE REQUEST: DataSpec file should be aware of its own location
        # Re: Why?
        self.name = ""
        self.creation_date = datetime.strptime(creation_date, "%Y.%m.%d_%H.%M.%S")
        self.experiment_date_time = None
        # FEATURE REQUEST: Allow multiple device types to be compatible with the same set
        self.device = ""
        self.notes = ""
        self.console = {}
        self.structure_type = None
        self.filepaths = {}
        self.colours = {}

    # Setters
    def set_name(self, name: str):
        assert isinstance(name, str)
        self.name = name

    def set_experiment_date(self, experiment_date_time: str):
        assert isinstance(experiment_date_time, str)
        self.experiment_date_time = datetime.strptime(experiment_date_time, "%Y.%m.%d_%H.%M.%S")

    def set_device(self, device: str):
        assert isinstance(device, str)
        self.device = device

    def set_structure_type(self, desired_type: str):
        try:
            assert desired_type in self._allowed_structure_types
        except AssertionError:
            raise ValueError

        if self.structure_type is None:
            self.structure_type = desired_type
        # Warn users when trying to overwrite the structure type

    def set_notes(self, notes_content: str):
        assert isinstance(notes_content, str)
        self.notes = notes_content

    def set_console(self, console_content: dict):
        assert isinstance(console_content, dict)
        self.console = console_content

    def set_filepaths(self, filepaths: dict):
        assert isinstance(filepaths, dict)
        self.filepaths = filepaths

    def set_colours(self, colours: dict):
        assert isinstance(colours, dict)
        self.colours = colours

    def construct_filepaths(self, root_dir: str, type: str) -> str:
        warnings.warn("New function construct_filepaths_nrecursive not implemented recursively")
        # TODO: Should depend on experiment type (making structure redundant)?
        # TODO: Something about the experiment type compatibility here.
        if type in self._allowed_structure_types:
            self.set_structure_type(type)
        else:
            return f"Incompatible structure type ({type}). Choose from {self._allowed_structure_types}"

        match type:
            case "flat":
                return self.construct_filepaths_nrecursive(root_dir)
            case "dirlabelled":
                return self.construct_structured_filepaths(root_dir)


    def construct_filepaths_nrecursive(self, root_dir) -> str:
        """
        Will generate a flat file set and add it to the current filepaths. This will seek all files and
            of the giver root_dir and append all dataspec files to the filepaths attribute. Note that
            root_dir should be an absolute path.
        """

        errors = ""
        # Checks which files are contained in the root dir
        items = natsort.natsorted(os.listdir(root_dir))
        for item in items:
            # Ignores duplicates
            if item in self.filepaths.keys():
                errors += f"Ignored {item}: duplicate label \n"
                continue

            # Only add valid files
            path = f"{root_dir}/{item}"
            is_path_valid, error_msg = self._check_valid_path(path)
            if is_path_valid:
                # Use filename as path label
                self.add_filepath(path=path, label=Path(path).stem)
            else:
                errors += error_msg

        return errors

    def construct_filepaths_recursive(self, root_dir) -> str:
        raise NotImplementedError

    def construct_structured_filepaths(self, root_dir: str) -> str:
        """
        Will generate a dirlabelled file set and add it to the current filepaths. This will seek all files and
            subdirectories of the giver root_dir and append all dataspec files to the filepaths attribute. Note that
            root_dir should be an absolute path.
        """
        warnings.warn("Function construct_structured_filepaths is deprecated use construct_filepaths instead", DeprecationWarning)
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
            errors = "Flat dataspec_manager cannot use dirlabelled construction"

        return errors

    # Getters
    def get_filepath(self, label: str) -> str:
        return self.filepaths[label]

    def get_filepaths(self) -> dict:
        return self.filepaths

    def get_experiment_date(self):
        return self.experiment_date_time

    def get_single_colour(self, label: str) -> str:
        if label in self.colours.keys():
            return self.colours[label]
        return None

    def get_all_colours(self) -> dict:
        if len(self.colours) == 0:
            return None
        return self.colours

    def get_labels(self):
        return self.filepaths.keys()

    def get_console(self) -> dict:
        return self.console

    def get_notes(self) -> str:
        return self.notes

    def get_structure_type(self) -> str:
        return self.structure_type

    def get_device(self) -> str:
        return self.device

    def get_creation_date(self) -> datetime:
        return self.creation_date

    def get_name(self) -> str:
        return self.name

    # Adding / Appending
    def add_notes(self, additional_notes: str):
        assert isinstance(additional_notes, str)
        self.notes += additional_notes

    def add_console(self, date_and_time: str, additional_console: str):
        assert isinstance(date_and_time, str)
        assert isinstance(additional_console, str)
        self.console[date_and_time] = additional_console

    # Path management
    def add_filepath(self, path: str, label: str):
        # Wrap flat paths for validation
        if self.get_structure_type() == 'flat':
            path_to_validate = {label: path}
        else:
            path_to_validate = path
        path_to_store = path

        # Check for duplicate label
        if label in self.filepaths.keys():
            return "Duplicate label found in dataspec_manager"

        # Check that all paths are valid
        for sublabel in path_to_validate:
            # Check path before adding:
            is_path_valid, error_msg = self._check_valid_path(path=path_to_validate[sublabel])
            if not is_path_valid:
                print(error_msg)
                return "Will not add file with disallowed extension"

        # Add the path
        self.filepaths[label] = path_to_store

        return ""

    def add_colour(self, colour: str, label: str):
        # Checks for duplicate label
        if label in self.colours.keys():
            return "Duplicate label found in colours"
        else:
            # Add the file to the dataset and update the gui
            self.colours[label] = colour

    # Checks are needed before paths are added to the dataspec_manager
    def _check_valid_path(self, path: str):
        assert isinstance(path, str)
        # Checks whether the path exists and points to a file
        if os.path.exists(path) and os.path.isfile(path):
            # Checks if the file has the proper extension
            if path.endswith(self._accepted_extensions):
                return True, ""
            else:
                return False, f"DataSpec Forbidden Extension: Ignored {path}\n"
        elif os.path.exists(path) and not os.path.isfile(path):
            return False, f"DataSpec Not a File: Ignored {path}\n"
        else:
            return False, f"DataSpec Filesystem Error: Ignored {path}\n"

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False
