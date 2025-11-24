from abc import ABC, abstractmethod
from contracts.data_processors import DataProcessor

class Plotter(ABC):
    @abstractmethod
    def ready_plot(self, processors: DataProcessor, options: dict):
        pass

    @abstractmethod
    def draw_plot(self):
        pass
