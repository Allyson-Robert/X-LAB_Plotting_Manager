from fileset.fileset import Fileset
from data.collections.scatter_collections.iv_scatter_collection import IVScatterCollection
from plotter.iv_plotter import IVScatterDataPlotter


class Sunbrick:
    def __init__(self):
        self.scatter_collection = None

    # FIXME: Not sure that Sunbrick should be the one to deal with the fileset.
    #   Possibly the ScatterCollection should be the one to deal with it.
    def set_data(self, fileset: Fileset):
        assert fileset.get_structure_type() == "flat"
        self.scatter_collection = IVScatterCollection(fileset.get_filepaths())

    def plot_fulliv(self, title, legend):
        plotter = IVScatterDataPlotter(title, "voltage", "current")
        self._scatter_plot(plotter, legend)

    def plot_iv(self, title, legend):
        plotter = IVScatterDataPlotter(title, "forward_voltage", "forward_current")
        self._scatter_plot(plotter, legend)

    def plot_fullpv(self, title, legend):
        plotter = IVScatterDataPlotter(title, "voltage", "power")
        self._scatter_plot(plotter, legend)

    def plot_pv(self, title, legend):
        plotter = IVScatterDataPlotter(title, "forward_voltage", "forward_power")
        self._scatter_plot(plotter, legend)

    def _scatter_plot(self, plotter: IVScatterDataPlotter, legend: str):
        plotter.ready_plot(self.scatter_collection, legend)
        plotter.draw_plot()

    def print_parameters(self, *args, **kwargs):
        data = self.scatter_collection.get_data()
        for lbl in data:
            iv_scatter_processor = data[lbl]
            print(iv_scatter_processor.get_data("parameters"))
