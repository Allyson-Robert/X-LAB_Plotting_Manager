from abc import ABC, abstractmethod


class Plotter(ABC):
    @abstractmethod
    def make_plot(self):
        pass