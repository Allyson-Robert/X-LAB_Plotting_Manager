from fileset.fileset import Fileset
from data.collections.scatter_collections.iv_scatter_collection import IVScatterCollection
from plotter.iv_plotter import IVScatterDataPlotter


class Sunbrick:
    def __init__(self):
        self.scatter_collection = None

    def set_data(self, fileset: Fileset):
        self.scatter_collection = IVScatterCollection(fileset.get_filepaths())

    def plot_fulliv(self, title, legend):
        test_plot = IVScatterDataPlotter(title, "voltage", "current")
        test_plot.ready_plot(self.scatter_collection, legend)
        test_plot.draw_plot()

    def plot_iv(self, title, legend):
        test_plot = IVScatterDataPlotter(title, "forward_voltage", "forward_current")
        test_plot.ready_plot(self.scatter_collection, legend)
        test_plot.draw_plot()

    def plot_fullpv(self, title, legend):
        test_plot = IVScatterDataPlotter(title, "voltage", "power")
        test_plot.ready_plot(self.scatter_collection, legend)
        test_plot.draw_plot()

    def plot_pv(self, title, legend):
        test_plot = IVScatterDataPlotter(title, "forward_voltage", "forward_power")
        test_plot.ready_plot(self.scatter_collection, legend)
        test_plot.draw_plot()

    def print_parameters(self, *args, **kwargs):
        data = self.scatter_collection.get_data()
        for lbl in data:
            iv_scatter_processor = data[lbl]
            print(iv_scatter_processor.get_data("parameters"))
