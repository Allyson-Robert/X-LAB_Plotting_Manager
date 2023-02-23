from data.datatypes.pds_data import PDSData
from data.data_processors.data_processors import DataProcessorCore


class PDSDataProcessor(DataProcessorCore):
    def __init__(self, data: PDSData):
        self.data = data

        self._processing_functions = {
            "signal": self.compute_signal,
            "signal_error": self.compute_signal_error,
        }

        self.processed_data = {}
        for key in self._processing_functions:
            self.processed_data[key] = None

        self._processed_observables = self.processed_data.keys()

    def validate_observables(self, *args) -> None:
        raise NotImplementedError

    def compute_signal(self):
        detector_a = self.get_data("a_sig")
        detector_b = self.get_data("b_sig")
        return {"units": "", "data": detector_b/detector_a}

    def compute_signal_error(self):
        detector_a = self.get_data("a_sig")
        detector_b = self.get_data("b_sig")
        detector_a_err = self.get_data("a_sig_err")
        detector_b_err = self.get_data("b_sig_err")
        signal = self.get_data("signal")

        signal_err = signal*(detector_b_err/detector_b + detector_a_err/detector_a)

        return {"units": "", "data": signal_err}
