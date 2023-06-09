from data.datatypes.data import DataCore
from utils.file_readers.read_csv import read_csv
from datetime import datetime
import re
import os


class IVData(DataCore):
    def __init__(self, label):
        super().__init__()
        self.raw_data = {
            "label": {"units": "N/A", "data": label},
            "voltage": None,
            "current": None,
            "datetime": None,
        }
        self._allowed_observables = self.raw_data.keys()
        self.label_format = "%Y_%m_%d_%H_%M_%S"
        self.dt_pattern = '\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}'

    # def get_data(self, observable: str):
    #     if observable in self._allowed_observables:
    #         return self.raw_data[observable]['data']
    #     else:
    #         raise ValueError(f"IVData does not contain {observable} data")
    #
    # def get_units(self, observable: str) -> str:
    #     self.get_data(observable)
    #     return self.raw_data[observable]["units"]
    #
    # def get_allowed_observables(self):
    #     return self._allowed_observables

    def read_file(self, filepath: str):
        data = read_csv(filepath)
        if self.raw_data['voltage'] is None:
            self.raw_data['voltage'] = {"units": "$Voltage ~(V)$", "data": data[0]}
        if self.raw_data['current'] is None:
            self.raw_data['current'] = {"units": "$Current ~(I)$", "data": data[1]}
        if self.raw_data['datetime'] is None:
            filename = os.path.basename(filepath)
            datetime_str = re.search(self.dt_pattern, filename)
            self.raw_data['datetime'] = {"units": None, "data": datetime.strptime(datetime_str.group(), self.label_format)}
