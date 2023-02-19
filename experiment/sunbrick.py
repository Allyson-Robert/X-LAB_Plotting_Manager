from data.data_processors.scatter_data.iv_data_processor import IVScatterDataProcessor
from data.datatypes.scatter_data.iv_scatter import IVScatterData
from experiment.experiment import Experiment
from plotter.scatter_data_plotter import ScatterDataPlotter
from fileset.fileset import Fileset


class Sunbrick(Experiment):
    def __init__(self):
        self.iv_data_processor = None

    def set_data(self, fileset: Fileset):
        assert fileset.get_structure_type() == "flat"

        filepaths = fileset.get_filepaths()
        self.iv_data_processor = {}
        for key in filepaths:
            iv_data = IVScatterData(key)
            iv_data.read_file(filepaths[key])
            self.iv_data_processor[key] = IVScatterDataProcessor(iv_data)

    def plot_fulliv(self, title, legend):
        plotter = ScatterDataPlotter(title, "voltage", "current")
        self._scatter_plot(plotter, legend)

    def plot_iv(self, title, legend):
        plotter = ScatterDataPlotter(title, "forward_voltage", "forward_current")
        self._scatter_plot(plotter, legend)

    def plot_fullpv(self, title, legend):
        plotter = ScatterDataPlotter(title, "voltage", "power")
        self._scatter_plot(plotter, legend)

    def plot_pv(self, title, legend):
        plotter = ScatterDataPlotter(title, "forward_voltage", "forward_power")
        self._scatter_plot(plotter, legend)

    def _scatter_plot(self, plotter: ScatterDataPlotter, legend: str):
        plotter.ready_plot(self.iv_data_processor, legend)
        plotter.draw_plot()

    def print_parameters(self, *args, **kwargs):
        for lbl in self.iv_data_processor:
            print(self.iv_data_processor[lbl].get_data("parameters"))
