from data.data_processors.data_processors import DataProcessorCore
from data.datatypes.lbic_image import LBICImage
from utils.calc.list_calc import flatten_matrix


class LBICImageProcessor(DataProcessorCore):
    def __init__(self, lbic_image: LBICImage):
        super().__init__(lbic_image)

        self.data = lbic_image
        self._processing_functions = {
            "current_list": self.flatten_currents
        }
        self.processed_data = {}
        for key in self._processing_functions:
            self.processed_data[key] = None

        self._processed_observables = self.processed_data.keys()

    def validate_observables(self, *args):
        # Checks whether all desired observables can be obtained for this data and catches relevant errors
        for observable in args:
            self.get_data(observable)

    def flatten_currents(self):
        data = flatten_matrix(self.get_data("current"))
        return {"units": "$Current (A)$", "data": data}
