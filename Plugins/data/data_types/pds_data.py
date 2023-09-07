from plugins.data.data_types.data import Data
from utils.file_readers.read_pds_file import read_pds_file


class PDSData(Data):
    def __init__(self, label):
        self.raw_data = {
            "header": None,
            "label": {"units": "N/A", "data": label},
            "time": None,
            "energy": None,
            "wavelength": None,
            "b_sig": None,
            "b_sig_err": None,
            "b_deg": None,
            "b_deg_error": None,
            "a_sig": None,
            "a_sig_err": None,
            "a_deg": None,
            "a_deg_error": None,
        }
        self._allowed_observables = self.raw_data.keys()

    def read_file(self, filepath: str) -> None:
        data = read_pds_file(filepath)

        if self.raw_data["header"] is None:
            self.raw_data["header"] = {"units": "", "data": data[0]}

        if self.raw_data["time"] is None:
            self.raw_data["time"] = {"units": "", "data": data[1]}

        if self.raw_data["energy"] is None:
            self.raw_data["energy"] = {"units": "$Energy ~(eV)$", "data": [float(x) for x in data[2]]}

        if self.raw_data["wavelength"] is None:
            self.raw_data["wavelength"] = {"units": "$Wavelength ~(nm)$", "data": [float(x) for x in data[3]]}

        if self.raw_data["b_sig"] is None:
            self.raw_data["b_sig"] = {"units": "$Lock-In B Amplitude ~(V)$", "data": [float(x) for x in data[4]]}

        if self.raw_data["b_sig_err"] is None:
            self.raw_data["b_sig_err"] = {"units": "$Lock-In B Amplitude Error ~(V)$", "data": [float(x) for x in data[5]]}

        if self.raw_data["b_deg"] is None:
            self.raw_data["b_deg"] = {"units": "$Lock-In B Phase ~(^circ)$", "data": [float(x) for x in data[6]]}

        if self.raw_data["b_deg_error"] is None:
            self.raw_data["b_deg_error"] = {"units": "$Lock-In B Phase Error ~(^circ)$", "data": [float(x) for x in data[7]]}

        if self.raw_data["a_sig"] is None:
            self.raw_data["a_sig"] = {"units": "Lock-In A Amplitude ~(V)", "data": [float(x) for x in data[8]]}

        if self.raw_data["a_sig_err"] is None:
            self.raw_data["a_sig_err"] = {"units": "Lock-In A Amplitude Error ~(V)", "data": [float(x) for x in data[9]]}

        if self.raw_data["a_deg"] is None:
            self.raw_data["a_deg"] = {"units": "$Lock-In A Phase ~(^circ)$", "data": [float(x) for x in data[10]]}

        if self.raw_data["a_deg_error"] is None:
            self.raw_data["a_deg_error"] = {"units": "$Lock-In A Phase Error ~(^circ)$", "data": [float(x) for x in data[11]]}

    def get_data(self, observable: str):
        if observable in self._allowed_observables:
            return self.raw_data[observable]['data']
        else:
            raise ValueError(f"PDSData does not contain {observable} data")

    def get_units(self, observable: str) -> str:
        self.get_data(observable)
        return self.raw_data[observable]["units"]

    def get_allowed_observables(self):
        return self._allowed_observables
