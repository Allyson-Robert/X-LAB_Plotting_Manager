from plugins.data.data_processors.data_processors import DataProcessor
from plugins.data.data_types import Data


class ScatterDataProcessorTest:
    def __init__(self, scatter_data: Data):
        self.scatter_data = scatter_data
        self.scatter_data_processor = None

    def test_init(self, scatter_data_processor: DataProcessor):
        self.scatter_data_processor = scatter_data_processor(self.scatter_data)

    def test_get_data(self):
        pass

    def test_get_units(self):
        pass

    def test_get_allowed_observables(self):
        pass

    def test_validate_observables(self):
        pass
