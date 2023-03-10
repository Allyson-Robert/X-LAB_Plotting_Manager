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

        self.set_data_type(IVData)
        self.set_processor_type(IVScatterDataProcessor)

    def set_options(self, *args, **kwargs):
        pass

    # def set_data(self, fileset: Fileset):
    #     assert fileset.get_structure_type() == "flat"
    #
    #     # Initialise an empty dict and get the required filepaths
    #     self.data_processors = {}
    #     filepaths = fileset.get_filepaths()
    #
    #     # Progress housekeeping
    #     nr_of_files = len(filepaths)
    #     counter = 0
    #
    #     # Read the data and instantiate a processor for each file
    #     for key in filepaths:
    #         iv_data = IVData(key)
    #         iv_data.read_file(filepaths[key])
    #         self.data_processors[key] = IVScatterDataProcessor(iv_data)
    #
    #         # Emit progress signal
    #         self.progress.emit(int(100*counter/nr_of_files))
    #         counter += 1

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
        plotter.ready_plot(self.data_processors, legend)
        plotter.draw_plot()

    def print_parameters(self, *args, **kwargs):
        for lbl in self.data_processors:
            print(self.data_processors[lbl].get_data("parameters"))
