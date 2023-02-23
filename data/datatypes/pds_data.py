from data.datatypes.data import Data
from utils.file_readers.read_csv import read_csv


class PDSData(Data):
    def __init__(self, label):
        self.raw_data = {
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
        # TODO: File header should also be read from the file, not just skipped
        data = read_csv(filepath, skip_lines=10)

        if self.raw_data["time"] is None:
            self.raw_data["time"] = {"units": "", "data": data[0]}

        if self.raw_data["energy"] is None:
            self.raw_data["energy"] = {"units": "", "data": float(data[1])}

        if self.raw_data["wavelength"] is None:
            self.raw_data["wavelength"] = {"units": "", "data": float(data[2])}

        if self.raw_data["b_sig"] is None:
            self.raw_data["b_sig"] = {"units": "", "data": float(data[3])}

        if self.raw_data["b_sig_err"] is None:
            self.raw_data["b_sig_err"] = {"units": "", "data": float(data[4])}

        if self.raw_data["b_deg"] is None:
            self.raw_data["b_deg"] = {"units": "", "data": float(data[5])}

        if self.raw_data["b_deg_error"] is None:
            self.raw_data["b_deg_error"] = {"units": "", "data": float(data[6])}

        if self.raw_data["a_sig"] is None:
            self.raw_data["a_sig"] = {"units": "", "data": float(data[7])}

        if self.raw_data["a_sig_err"] is None:
            self.raw_data["a_sig_err"] = {"units": "", "data": float(data[8])}

        if self.raw_data["a_deg"] is None:
            self.raw_data["a_deg"] = {"units": "", "data": float(data[9])}

        if self.raw_data["a_deg_error"] is None:
            self.raw_data["a_deg_error"] = {"units": "", "data": float(data[11])}

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
