from data.data_processors.data_processors import DataProcessorCore
from data.datatypes.scatter_data.fluorescence_scatter import FluorescenceData


class FluorescenceScatterDataProcessor(DataProcessorCore):
    def __init__(self, fluorescence_data: FluorescenceData):
        super().__init__(fluorescence_data)

    def validate_observables(self, *args):
        print(*args)
        # Checks whether all desired observables can be obtained for this data
        try:
            for observable in args:
                self.get_data(observable)
        # TODO: Catchall try-except
        except:
            raise
