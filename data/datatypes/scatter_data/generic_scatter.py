from data.datatypes.data import DataCore
from utils.file_readers.read_csv import read_csv


class GenericScatterData(DataCore):
    def __init__(self, label):
        super().__init__()
        self.raw_data = {
            "label": {"units": "N/A", "data": label},
            "independent": None,
            "dependent": None,
            "datetime": None,
        }
        self._allowed_observables = self.raw_data.keys()
        self.label_format = "%Y_%m_%d_%H_%M_%S"
        self.dt_pattern = '\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}'

    def read_file(self, filepath: str):
        data = read_csv(filepath)
        if self.raw_data['independent'] is None:
            self.raw_data['independent'] = {"units": "Independent var (a.u.)", "data": data[0]}
        if self.raw_data['dependent'] is None:
            self.raw_data['dependent'] = {"units": "Dependent var (a.u.)", "data": data[1]}
