from data.datatypes.data import DataCore
from utils.file_readers.read_lbic import read_lbic


class LBICImage(DataCore):
    def __init__(self, label):
        super().__init__()
        self.raw_data = {
            "label": {"units": "N/A", "data": label},
            "x_axis": None,
            "y_axis": None,
            "current": None,
        }
        self._allowed_observables = self.raw_data.keys()

    def read_file(self, filepath: str) -> None:
        data = read_lbic(filepath)
        if self.raw_data['x_axis'] is None:
            self.raw_data['x_axis'] = {"units": "$X-Position ~(mm)$", "data": data[0]}
        if self.raw_data['y_axis'] is None:
            self.raw_data['y_axis'] = {"units": "Y-position ~(mm)$", "data": data[1]}
        if self.raw_data['current'] is None:
            self.raw_data['current'] = {"units": "Current ~(A)$", "data": data[2]}
