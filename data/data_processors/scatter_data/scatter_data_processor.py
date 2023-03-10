from data.data_processors.data_processors import DataProcessorCore
from data.datatypes.scatter_data.generic_scatter import GenericData
from utils.errors.errors import ObservableNotComputableError


class ScatterDataProcessor(DataProcessorCore):
    def __init__(self, absorbance_data: GenericData):
        super().__init__(absorbance_data)

    def validate_observables(self, *args):
        print(*args)
        # Checks whether all desired observables can be obtained for this data
        try:
            for observable in args:
                self.get_data(observable)
        # TODO: Catchall try-except
        except:
            raise ObservableNotComputableError
