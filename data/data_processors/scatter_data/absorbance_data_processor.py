from data.data_processors.scatter_data.data_processors import ScatterDataProcessor
from data.datatypes.scatter_data.absorbance_scatter import AbsorbanceScatterData


class AbsorbanceScatterDataProcessor(ScatterDataProcessor):
    def __init__(self, absorbance_data: AbsorbanceScatterData):
        self.data = absorbance_data

        self._processing_functions = {
        }

        self.processed_data = {}
        for key in self._processing_functions:
            self.processed_data[key] = None

        self._processed_observables = self.processed_data.keys()

    # TODO: This is a dup from IVScatterDataProcessor
    def get_data(self, observable: str):
        # Returns the requested raw data
        if observable in self.data.get_allowed_observables():
            return self.data.get_data(observable)

        # Compute processed data if needed
        elif observable in self._processed_observables:
            if self.processed_data[observable] is None:
                self.processed_data[observable] = self._processing_functions[observable]()
            return self.processed_data[observable]['data']
        else:
            raise ValueError(f"IVScatterData does not contain {observable} data")

    # TODO: This is a dup from IVScatterDataProcessor
    def get_units(self, observable: str) -> str:
        self.get_data(observable)
        # Return raw data
        if observable in self.data.get_allowed_observables():
            return self.data.get_units(observable)
        elif observable in self._processed_observables:
            return self.processed_data[observable]["units"]
        else:
            raise ValueError(f"IVScatterData does not contain {observable} data")

    # TODO: This is a dup from IVScatterDataProcessor
    # TODO: Is this really necessary? Ignores Datatype observables
    def get_allowed_observables(self):
        return self._processed_observables

    def validate_observables(self, *args):
        print(*args)
        # Checks whether all desired observables can be obtained for this data
        try:
            for observable in args:
                self.get_data(observable)
        # TODO: Catchall try-except
        except:
            raise ObservableNotComputableError
