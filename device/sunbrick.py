from fileset.fileset import Fileset
from data.collections.scatter_collections.iv_scatter_collection import IVScatterCollection
from plotter.iv_plotter import IVPlotter


class Sunbrick:
    def __init__(self):
        self.scatter_collection = None

    def set_data(self, fileset: Fileset):
        self.scatter_collection = IVScatterCollection(fileset.get_filepaths())

    def plot_fulliv(self, title, legend):
        test_plot = IVPlotter(title, legend)
        test_plot.ready_plot()
        test_plot.draw_plot(self.scatter_collection)
