from data.data_processors.iv_data_processor import IVScatterDataProcessor
from data.data_processors.data_processors import ScatterDataProcessor
from data.datatypes.scatter_data.iv_scatter import IVScatterData


class IVStabilityDataProcessor(ScatterDataProcessor):
    """
        This class will utilise the ScatterDataProcessor in order to compute physical quantities related to stability
            measurements.
            This class therefore needs access to IVScatterDataProcessor in order to obtain the quantities from
            IVScatterData.
        This should contain the entire time evolution of a solar cell and so needs a list of IVScatterData to process.
    """
    def __init__(self, iv_data_list: list[IVScatterData]):
        self.data = iv_data_list

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
        self.processed_data = {}
        for key in self._processing_functions:
            self.processed_data[key] = None

        # Check illumination status of all files immediately -> further data cannot be made available for dark meas.
        self.illuminated = self.get_time_evolved("is_illuminated")

    def get_data(self, observable: str):
        # Compute processed data if needed
        if observable in self.processed_data.keys():
            if self.illuminated:
                if self.processed_data[observable] is None:
                    self.processed_data[observable] = self._processing_functions[observable](observable)
                return self.processed_data[observable]['data']
            else:
                raise ValueError(f"IVScatterDataProcessor contains dark measurements")
        else:
            raise ValueError(f"IVScatterDataProcessor does not contain {observable} data")

    def get_units(self, observable: str) -> str:
        # Return raw data
        if observable in self.processed_data.keys():
            return self.processed_data[observable]['units']
        else:
            raise ValueError(f"IVScatterDataProcessor does not contain {observable} data")

    def get_time_evolved(self, observable):
        # TODO: Skip the dark measurements
        measurements = []
        for iv_data in self.data:
            processor = IVScatterDataProcessor(iv_data)
            measurements.append(processor.get_data(observable))
        units = processor.get_units(observable)
        return {"units": units, "data": measurements}

    def get_time_differences(self, *args, **kwargs):
        # Ignore *args, **kwargs, only needed to remain compatible with get_data
        datetimes = self.get_time_evolved("datetime")["data"]
        time_diff_list = [(dt - datetimes[0]).total_seconds()/3600 for dt in datetimes]
        return {"units": "Elapsed time (hrs)", "data": time_diff_list}
