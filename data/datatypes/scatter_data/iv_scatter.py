from data.datatypes.scatter_data.scatter import ScatterData
from utils.file_readers.read_csv import read_csv


class IVScatterData(ScatterData):
    def __init__(self, label):
        self.data = {
            "label": label,
            "voltage": [],
            "current": []
        }
        self._allowed_observables = self.data.keys()

    def get_data(self, observable: str) -> list:
        if observable in self._allowed_observables:
            return self.data[observable]

    def read_file(self, filepath: str):
        data = read_csv(filepath)
        self.data['voltage'] = data[0]
        self.data['current'] = data[1]
