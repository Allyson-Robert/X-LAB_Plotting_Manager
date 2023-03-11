from data.data_processors.data_processors import DataProcessorCore
from data.datatypes.lbic_image import LBICImage


class LBICImageProcessor(DataProcessorCore):
    def __init__(self, lbic_image: LBICImage):
        super().__init__(lbic_image)

    def validate_observables(self, *args):
        # Checks whether all desired observables can be obtained for this data and catches relevant errors
        for observable in args:
            self.get_data(observable)
