from data.data_processors.scatter_data.data_processors import ScatterDataProcessor
from data.datatypes.scatter_data.scatter import ScatterData


class ScatterDataProcessorTest:
    def __init__(self, scatter_data: ScatterData):
        self.scatter_data = scatter_data
        self.scatter_data_processor = None

    def test_init(self, scatter_data_processor: ScatterDataProcessor):
        self.scatter_data_processor = scatter_data_processor(self.scatter_data)

    def test_get_data(self):
        pass

    def test_get_units(self):
        pass

    def test_get_allowed_observables(self):
        pass

    def test_validate_observables(self):
        pass
