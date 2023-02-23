from data.data_processors.scatter_data.data_processors import ScatterDataProcessorCore
from data.datatypes.scatter_data.fluorescence_scatter import FluorescenceScatterData


class FluorescenceScatterDataProcessor(ScatterDataProcessorCore):
    def __init__(self, absorbance_data: FluorescenceScatterData):
        self.data = absorbance_data

        self._processing_functions = {
        }

        self.processed_data = {}
        for key in self._processing_functions:
            self.processed_data[key] = None

        self._processed_observables = self.processed_data.keys()

    def validate_observables(self, *args):
        print(*args)
        # Checks whether all desired observables can be obtained for this data
        try:
            for observable in args:
                self.get_data(observable)
        # TODO: Catchall try-except
        except:
            raise
