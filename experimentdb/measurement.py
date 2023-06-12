import os
import re
from datetime import datetime


class Measurement:
    _accepted_extensions = ("xlsx", "xls", "csv", "txt")

    def __init__(self, filepath: str, label: str):
        assert isinstance(label, str)
        self._check_valid_path(filepath)
        self.location = filepath

        self.label = ""

        self.datetime = None
        self.set_datetime()

        self.colour = None

    def set_datetime(self):
        dt_pattern = '\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}'
        datetime_str = re.search(dt_pattern, os.path.basename(self.get_location()))
        self.datetime = datetime.strptime(datetime_str.group(), "%Y_%m_%d_%H_%M_%S")

    def get_datetime(self):
        return self.datetime

    def set_colour(self, colour):
        self.colour = colour

    def get_colour(self):
        if self.colour is None:
            raise AttributeError("Measurement colour not set")
        return self.colour

    def get_location(self):
        if self.location is None:
            raise AttributeError("Measurement location not set")
        return self.location

    def _check_valid_path(self, path: str):
        assert isinstance(path, str)
        # Checks whether the path exists and points to a file
        if os.path.exists(path) and os.path.isfile(path):
            # Checks if the file has the proper extension
            if not path.endswith(self._accepted_extensions):
                raise ValueError(f"Forbidden Extension: Ignored {path}\n")
        elif os.path.exists(path) and not os.path.isfile(path):
            raise ValueError(f"Filesystem Error: Not a File: Ignored {path}\n")

        else:
            raise ValueError(f"Filesystem Error: {path} does not exist\n")
        return True