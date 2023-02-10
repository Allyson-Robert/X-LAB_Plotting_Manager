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
    def __init__(self, iv_data: list[IVScatterData]):
        self.data = iv_data

        self.processed_data = {
            "isc": None,
            "voc": None,
            "mpp_power": None,
            "fill_factor": None,
            "series_resistance": None,
            "shunt_resistance": None,
            "parameters": None
        }

    def get_data(self, observable: str):
        # Compute processed data if needed
        if observable in self.processed_data.keys():
            if self.processed_data[observable] is None:
                self.processed_data[observable] = self.get_time_evolved(observable)
            return self.processed_data[observable]['data']
        else:
            raise ValueError(f"IVScatterDataProcessor does not contain {observable} data")

    def get_units(self, observable: str) -> str:
        # Return raw data
        if observable in self.processed_data.keys():
            return self.processed_data[observable]['units']
        else:
            raise ValueError(f"IVScatterDataProcessor does not contain {observable} data")

    def get_time_evolved(self, observable):
        measurements = []
        for iv_data in self.data:
            processor = IVScatterDataProcessor(iv_data)
            measurements.append(processor.get_data(observable))
        units = processor.get_units(observable)
        return {"units": units, "data": measurements}
