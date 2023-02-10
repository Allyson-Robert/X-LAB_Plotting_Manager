from abc import ABC, abstractmethod
from data.data_processors.data_processors import ScatterDataProcessor


class Plotter(ABC):
    @abstractmethod
    def ready_plot(self, processors: ScatterDataProcessor, legend_title: str):
        pass

    @abstractmethod
    def draw_plot(self):
        pass