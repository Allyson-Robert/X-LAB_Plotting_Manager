from data.data_processors.scatter_data.iv_data_processor import IVScatterDataProcessor
from data.datatypes.scatter_data.iv_scatter import IVData
from experiment.experiment_worker import ExperimentWorkerCore
from plotter.scatter_data_plotter import ScatterDataPlotter
from fileset.fileset import Fileset


class Sunbrick(ExperimentWorkerCore):
    """
         Implements the plotting function for the Sunbrick experiment.
         Relevant data types and processors are IVData and IVScatterDataProcessor.
    """
    def __init__(self, device, fileset, plot_type, legend):
        super().__init__(device, fileset, plot_type, legend)

        # Initialise an empty dict and get the required filepaths
        self.iv_data_processor = {}
        filepaths = fileset.get_filepaths()

        # Progress housekeeping
        nr_of_files = len(filepaths)
        counter = 0

        # Read the data and instantiate a processor for each file
        for key in filepaths:
            iv_data = IVData(key)
            iv_data.read_file(filepaths[key])
            self.iv_data_processor[key] = IVScatterDataProcessor(iv_data)

            # Emit progress signal
            self.progress.emit(int(100*counter/nr_of_files))
            counter += 1

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
