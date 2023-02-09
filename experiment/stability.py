from fileset.fileset import Fileset
from data.collections.scatter_collections.iv_structured_collection import IVStructuredCollection
from plotter.iv_stability_plotter import IVStabilityPlotter


class Stability:
    def __init__(self):
        self.scatter_collection = None

    def set_data(self, fileset: Fileset):
        assert fileset.get_structure_type() == "structured"
        self.scatter_collection = IVStructuredCollection(fileset.get_filepaths())

    def plot_four(self, title, legend):
        plotter = IVStabilityPlotter(title)
        plotter.ready_plot(self.scatter_collection, legend)
        plotter.draw_plot()
