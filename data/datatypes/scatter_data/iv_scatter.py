from data.datatypes.scatter_data.scatter import ScatterData
from utils.file_readers.read_csv import read_csv


class IVScatterData(ScatterData):
    def __init__(self, label):
        self.raw_data = {
            "label": label,
            "voltage": [],
            "current": [],
        }
        self._allowed_observables = self.raw_data.keys()

    def get_data(self, observable: str) -> list:
        if observable in self._allowed_observables:
            return self.raw_data[observable]
        else:
            raise ValueError(f"IVScatterData does not contain {observable} data")

    def get_allowed_observables(self):
        return self._allowed_observables

    def read_file(self, filepath: str):
        data = read_csv(filepath)
        self.raw_data['voltage'] = data[0]
        self.raw_data['current'] = data[1]
