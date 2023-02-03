import os
import natsort


class Fileset:
    """
    This class collects paths to files containing relevant data. The exact contents of the files does not matter as
    only the locations are relevant for this class.
    Paths can be added by construction in which case the structure type is said to be 'structured'. Paths can also be
    added manually one by one, in this case the structure type is 'flat'. Should a Fileset instance add files manually
    as well as by construction then the structure type is 'semi-structured' and the Fileset will need to be pruned later
    on.
    """
    _allowed_structure_types = ("flat", "structured", "semi_structured")
    _accepted_extensions = ("xlsx", "xls", "csv", "txt")

    def __init__(self, name, date, device):
        assert isinstance(name, str)
        assert isinstance(date, str)
        assert isinstance(device, str)

        self.name = name
        self.date = date
        self.device = device
        self.notes = ""
        self.console = ""
        self.structure_type = ""
        self.filepaths = {}

    # All defined during initialisation
    def get_name(self):
        return self.name

    def get_date(self):
        return self.date

    def get_device(self):
        return self.device

    def get_structure_type(self):
        return self.structure_type

    def _set_structure_type(self, current_type):
        """
        Set the structure type if it has not been set yet. Otherwise, check whether the type differs from the previous
        one. If they do differ then the structure is always semi_structured.
        """
        assert current_type in self._allowed_structure_types
        if self.structure_type is None:
            self.structure_type = current_type
        else:
            if self.structure_type != current_type:
                self.structure_type = "semi_structured"

    # These can be added later
    def set_notes(self, notes_content):
        assert isinstance(notes_content, str)
        self.notes = notes_content

    def get_notes(self):
        return self.notes

    def set_console(self, console_content):
        assert isinstance(console_content, str)
        self.console = console_content

    def get_console(self):
        return self.console

    # Path management
    def add_filepath(self, path, label):
        # Check for duplicate label
        if label in self.filepaths.keys():
            return "Duplicate label found in fileset"
        else:
            # Add the file to the dataset and update the GUI
            self.filepaths[label] = path

        self._set_structure_type("flat")
        return ""

    def construct_flat_filepaths(self, root_dir):
        """
        This smells
        Meant to add an entire directory in one go but without needing the structure.
        """
        pass

    def construct_structured_filepaths(self, root_dir):
        """
        Will generate a structured file set and add it to the current filepaths. This will seek all files and
            subdirectories of the giver root_dir and append all data files to the filepaths attribute. Note that
            root_dir should be an absolute path.
        """

        errors = ""
        items = natsort.natsorted(os.listdir(root_dir))
        for item in items:
            if item in self.filepaths.keys():
                errors += f"Ignored {item}: duplicate label \n"
                continue

            # If the item is a file add it directly
            path = f"{root_dir}/{item}"
            if os.path.isfile(path):
                self.filepaths[item] = path

            # Create nested dict for subdirectories
            else:
                self.filepaths[item] = {}
                for file in natsort.natsorted(os.listdir(path)):
                    # Only append to dataset if file is actually a file with an accepted extension
                    filepath = f"{path}/{file}"
                    if os.path.exists(filepath) and os.path.isfile(filepath):
                        if file.endswith(self._accepted_extensions):
                            self.filepaths[item][file] = filepath
                        else:
                            errors += f"Ignored {item}/{file}: extension not allowed\n"

                    # Ignore items that are not actually files
                    elif os.path.isfile(filepath):
                        errors += f"Ignored {item}/{file}: not a file\n"

                    # Filesystem issues can result in os.path.exists() returning false
                    else:
                        errors += f"Ignored {item}/{file}: filesystem error\n"

        self._set_structure_type("structured")

        return errors

    def get_filepaths(self):
        return self.filepaths
