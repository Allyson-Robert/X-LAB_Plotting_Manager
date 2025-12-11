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

        Known Limitations:
            Implmentations will be instantiated by worker threads relying on PyQt. This means that usage of matplotlib
            should be restricted to non-interactive modes only (e.g., 'Agg') to avoid GUI conflicts. This behaviour can
            currently not be changed and failure to comply may lead to runtime errors and crashes when calling fig.show().
            Ensure matplotlib is set to use the 'Agg' backend when importing.

            import matplotlib
            matplotlib.use("Agg")  # safe for worker threads
    """
    @abstractmethod
    def ready_plot(self, processors: DataProcessor, options: dict):
        pass

    @abstractmethod
    def draw_plot(self):
        pass
