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

    def validate_observables(self, *args):
        # Checks whether all desired observables can be obtained for this data and catches relevant errors
        for observable in args:
            self.get_data(observable)

    def compute_signal(self):
        detector_a = self.get_data("a_sig")
        detector_b = self.get_data("b_sig")

        signal = []
        for i in range(len(detector_a)):
            signal.append(detector_b[i]/detector_a[i])

        return {"units": "Signal (unitless)", "data": signal}

    def compute_signal_error(self):
        detector_a = self.get_data("a_sig")
        detector_b = self.get_data("b_sig")
        detector_a_err = self.get_data("a_sig_err")
        detector_b_err = self.get_data("b_sig_err")
        signal = self.get_data("signal")

        signal_err = []
        for i in range(len(detector_a)):
            signal_err.append(signal[i]*(detector_b_err[i]/detector_b[i] + detector_a_err[i]/detector_a[i]))

        return {"units": "Signal error (unitless)", "data": signal_err}
