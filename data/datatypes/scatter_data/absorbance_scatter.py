from data.datatypes.scatter_data.scatter import ScatterData
from utils.file_readers.read_csv import read_csv
import pandas as pd
from datetime import datetime
import re
import os


class AbsorbanceScatterData(ScatterData):
    def __init__(self, label):
        # TODO: Datetime should be added, time resolved measurements will be needed, such as DPBF experiments
        self.raw_data = {
            "label": {"units": "N/A", "data": label},
            "wavelength": None,
            "absorbance": None,
            # "datetime": None,
        }
        self._allowed_observables = self.raw_data.keys()
        # self.label_format = "%Y_%m_%d_%H_%M_%S"
        # self.dt_pattern = '\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}'

    def read_file(self, filepath: str):
        # TODO: Maybe there is a better way to do this?
        if 'xls' in filepath.split('.')[-1]:
            return pd.read_excel(filepath)
        else:
            data = read_csv(filepath)
            # TODO: Some files have the first row removed, others do not
            self.raw_data['wavelength'] = {"units": "$Wavelength ~(nm)$", "data": data[0][1:]}
            self.raw_data['absorbance'] = {"units": "$Absorbance ~(a.u.)$", "data": data[1][1:]}

    def get_data(self, observable: str) -> list:
        if self.raw_data[observable] is not None:
            if observable in self._allowed_observables:
                return self.raw_data[observable]['data']
            else:
                raise ValueError(f"AbsorbanceScatterData does not contain {observable} data")
        else:
            raise ValueError(f"Data has not been read from file for {self}")

    def get_units(self, observable: str) -> str:
        self.get_data(observable)
        return self.raw_data[observable]['units']

    def get_allowed_observables(self):
        return self._allowed_observables
