from data.data_processors.scatter_data.iv_data_processor import IVScatterDataProcessor
from data.data_processors.data_processors import DataProcessor
from data.datatypes.scatter_data.iv_scatter import IVData
from utils.errors.errors import ObservableNotComputableError
from datetime import datetime


class IVStabilityDataProcessor(DataProcessor):
    """
    This class will utilise the DataProcessor in order to compute physical quantities related to stability
        measurements. These are fundamentally about the time evolution of IV parameters.
        This class defers the computation of all observables to IVScatterDataProcessor with the notable exception
        being the elapsed time between any IV curve and the start of the device.
    """
    def __init__(self, iv_data_list: list[IVData], start_time: datetime):
        self.processors = [IVScatterDataProcessor(iv_data) for iv_data in iv_data_list]

        # Keep track of the function required to gather the data for the following observables
        self._processing_functions = {
            "time_differences": self.get_time_differences,
            "isc": self.get_time_evolved,
            "voc": self.get_time_evolved,
            "mpp_power": self.get_time_evolved,
            "fill_factor": self.get_time_evolved,
            "series_resistance": self.get_time_evolved,
            "shunt_resistance": self.get_time_evolved,
            "parameters": self.get_time_evolved
        }

        # Hold the data
        self.processed_data = {}
        for key in self._processing_functions:
            self.processed_data[key] = None

        # Hold device start time
        self.start_time = start_time

    def validate_observables(self, *args):
        """
        Checks if any of the observables generates a non-crucial error. If it does the processor is excluded and the data
        is effectively ignored.
        """
        rejected_processors = []
        for processor in self.processors:
            try:
                processor.validate_observables(*args)
            except ObservableNotComputableError:
                # FEATURE REQUEST: Inform user that this processor could not compute one of the observables
                rejected_processors.append(processor)

        for processor in rejected_processors:
            self.processors.remove(processor)

        return [processor.get_data("label") for processor in rejected_processors]

    def get_data(self, observable: str, *args, **kwargs):
        # Compute processed data if needed
        if observable in self.processed_data.keys():
            if self.processed_data[observable] is None:
                self.processed_data[observable] = self._processing_functions[observable](observable)
            return self.processed_data[observable]['data']
        else:
            raise ValueError(f"IVScatterDataProcessor does not contain {observable} data")

    def get_units(self, observable: str) -> str:
        # Return raw data
        if observable in self.processed_data.keys():
            return self.processed_data[observable]['units']
        else:
            raise ValueError(f"IVScatterDataProcessor does not contain {observable} data")

    # FIXME: Type hint using TypedDict https://peps.python.org/pep-0589/
    def get_time_evolved(self, observable: str):
        measurements = []
        units = ""
        for processor in self.processors:
            # Ignore data when either Voc or Isc cannot be found
            measurements.append(processor.get_data(observable))
            units = processor.get_units(observable)

        return {"units": units, "data": measurements}

    def get_time_differences(self, *args, **kwargs) -> dict:
        # Ignore *args, **kwargs, only needed to remain compatible with get_data
        datetime_list = self.get_time_evolved("datetime")["data"]
        time_diff_list = [(dt - self.start_time).total_seconds()/3600 for dt in datetime_list]

        return {"units": "Elapsed time (hrs)", "data": time_diff_list}
