from data.datatypes.data import Data
from utils.file_readers.read_csv import read_csv
from datetime import datetime
import re
import os

class GenericData(Data):
    def __init__(self, label):
        self.raw_data = {
            "label": {"units": "N/A", "data": label},
            "independent": None,
            "dependent": None,
            "datetime": None,
        }
        self._allowed_observables = self.raw_data.keys()
        self.label_format = "%Y_%m_%d_%H_%M_%S"
        self.dt_pattern = '\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}'

    def get_data(self, observable: str):
        if observable in self._allowed_observables:
            return self.raw_data[observable]['data']
        else:
            raise ValueError(f"IVData does not contain {observable} data")

    def get_units(self, observable: str) -> str:
        self.get_data(observable)
        return self.raw_data[observable]["units"]

    def get_allowed_observables(self):
        return self._allowed_observables

    def read_file(self, filepath: str):
        data = read_csv(filepath)
        if self.raw_data['independent'] is None:
            self.raw_data['independent'] = {"units": "$Time ~(a.u.)$", "data": data[0]}
        if self.raw_data['dependent'] is None:
            self.raw_data['dependent'] = {"units": "$Power ~(W)$", "data": data[1]}
