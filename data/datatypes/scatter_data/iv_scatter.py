from data.datatypes.scatter_data.scatter import ScatterData
from utils.file_readers.read_csv import read_csv


class IVScatterData(ScatterData):
    def __init__(self, label):
        self.raw_data = {
            "label": {"units": "N/A", "data": label},
            "voltage": None,
            "current": None,
        }
        self._allowed_observables = self.raw_data.keys()

    def get_data(self, observable: str) -> list:
        if observable in self._allowed_observables:
            return self.raw_data[observable]['data']
        else:
            raise ValueError(f"IVScatterData does not contain {observable} data")

    def get_units(self, observable: str) -> str:
        self.get_data(observable)
        return self.raw_data[observable]["units"]

    def get_allowed_observables(self):
        return self._allowed_observables

    def read_file(self, filepath: str):
        data = read_csv(filepath)
        if self.raw_data['voltage'] is None:
            self.raw_data['voltage'] = {"units": "Voltage (V)", "data": data[0]}
        if self.raw_data['current'] is None:
            self.raw_data['current'] = {"units": "Current (I)", "data": data[1]}
