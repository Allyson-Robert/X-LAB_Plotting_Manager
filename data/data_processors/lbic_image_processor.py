from data.data_processors.data_processors import DataProcessorCore
from data.datatypes.lbic_image import LBICImage
from utils.calc.list_calc import flatten_matrix
import numpy as np


class LBICImageProcessor(DataProcessorCore):
    def __init__(self, lbic_image: LBICImage):
        super().__init__(lbic_image)

        self.data = lbic_image
        self._processing_functions = {
            "current_list": self.flatten_currents,
            "horizontal_profile": self.get_horizontal_profile,
            "vertical_profile": self.get_vertical_profile,
            "diagonal_profile": self.get_diagonal_profile
        }
        self.processed_data = {}
        for key in self._processing_functions:
            self.processed_data[key] = None

        self._processed_observables = self.processed_data.keys()

    def validate_observables(self, *args):
        # Checks whether all desired observables can be obtained for this data and catches relevant errors
        for observable in args:
            self.get_data(observable)

    def get_data(self, observable: str, *args, **kwargs):
        # If observable is from raw data delegate to Data
        if observable in self.data.get_allowed_observables():
            return self.data.get_data(observable)

        # Compute processed data if needed
        if observable in self.processed_data.keys():
            if self.processed_data[observable] is None:
                self.processed_data[observable] = self._processing_functions[observable](*args, **kwargs)
            return self.processed_data[observable]['data']
        else:
            raise ValueError(f"LBICImageProcessor does not contain {observable} data")

    def flatten_currents(self, *args, **kwargs):
        data = flatten_matrix(self.get_data("current"))
        return {"units": "$Current (A)$", "data": data}

    def get_horizontal_profile(self, y_position: float = 0.0, *args, **kwargs):
        profile_index = np.abs([yval - y_position for yval in self.get_data("y_axis")]).argmin()
        data = self.get_data("current")[profile_index]
        return {"units": "$Current ~(A)$", "data": data}

    def get_vertical_profile(self, *args, **kwargs):
        pass

    def get_diagonal_profile(self, *args, **kwargs):
        pass
