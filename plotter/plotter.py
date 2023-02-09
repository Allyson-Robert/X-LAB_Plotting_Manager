from abc import ABC, abstractmethod
from data.collections.scatter_collections.scatter_collection import ScatterCollection


class Plotter(ABC):
    @abstractmethod
    def ready_plot(self, collection: ScatterCollection, legend_title: str):
        pass

    @abstractmethod
    def draw_plot(self):
        pass