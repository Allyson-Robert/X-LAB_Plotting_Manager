from abc import ABC, abstractmethod
from data.data_processors.data_processors import DataProcessor


class Plotter(ABC):
    @abstractmethod
    def ready_plot(self, processors: DataProcessor, legend_title: str):
        pass

    @abstractmethod
    def draw_plot(self):
        pass
