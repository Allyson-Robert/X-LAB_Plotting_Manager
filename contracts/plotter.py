from abc import ABC, abstractmethod
from contracts.data_processors import DataProcessor

class Plotter(ABC):
    """
        Abstract plotting interface for rendering data from processors.

        Overview:
            Specifies the minimal lifecycle for a plot: prepare with processors
            and options, then draw.

        - Abstract methods: ready_plot(processors, options) and draw_plot().
        - Intended to separate data preparation from rendering.

        Usage Notes:
            Implementations should be lightweight and accept a DataProcessor instance.
    """
    @abstractmethod
    def ready_plot(self, processors: DataProcessor, options: dict):
        pass

    @abstractmethod
    def draw_plot(self):
        pass
