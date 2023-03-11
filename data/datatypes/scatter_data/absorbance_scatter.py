from data.datatypes.data import DataCore
from utils.file_readers.read_csv import read_csv
import pandas as pd


class AbsorbanceData(DataCore):
    def __init__(self, label):
        super().__init__()
        self.raw_data = {
            "label": {"units": "N/A", "data": label},
            "wavelength": None,
            "absorbance": None,
            # "datetime": None,
        }
        self._allowed_observables = self.raw_data.keys()
        # TODO: Datetime should be added, time resolved measurements will be needed, such as DPBF experiments
        # self.label_format = "%Y_%m_%d_%H_%M_%S"
        # self.dt_pattern = '\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}'

    def read_file(self, filepath: str):
        if 'xls' in filepath.split('.')[-1]:
            data = pd.read_excel(filepath, header=None)
            x_data = data[data.keys()[0]]
            y_data = data[data.keys()[1]]
        else:
            data = read_csv(filepath)
            x_data = data[0][1:]
            y_data = data[1][1:]

        # If the very first element of the first column is a 0 then there's a headewr t
        if x_data[0] == 0:
            x_data = x_data[1:]
            y_data = y_data[1:]

        self.raw_data['wavelength'] = {"units": "$Wavelength ~(nm)$", "data": x_data}
        self.raw_data['absorbance'] = {"units": "$Absorbance ~(a.u.)$", "data": y_data}
