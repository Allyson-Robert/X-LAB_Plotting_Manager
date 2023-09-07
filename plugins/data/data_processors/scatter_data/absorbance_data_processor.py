from plugins.data.data_processors.data_processors import DataProcessorCore
from plugins.data.data_types.scatter_data.absorbance_scatter import AbsorbanceData
from utils.errors.errors import ObservableNotComputableError


class AbsorbanceScatterDataProcessor(DataProcessorCore):
    def __init__(self, absorbance_data: AbsorbanceData):
        self.data = absorbance_data

        self._processing_functions = {
        }

        self.processed_data = {}
        for key in self._processing_functions:
            self.processed_data[key] = None

        self._processed_observables = self.processed_data.keys()

    def validate_observables(self, *args):
        # Checks whether all desired observables can be obtained for this data
        try:
            for observable in args:
                self.get_data(observable)
        # FIXME: Catchall try-except
        except:
            raise ObservableNotComputableError
