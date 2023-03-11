from experiment.experiment_worker import ExperimentWorkerCore
from plotter.scatter_data_plotter import ScatterDataPlotter
from data.datatypes.pds_data import PDSData
from data.data_processors.pds_data_processor import PDSDataProcessor


class PDS(ExperimentWorkerCore):
    def __init__(self, device, fileset, plot_type, legend, options):
        # super() delegates method calls to a parent
        super().__init__(device, fileset, plot_type, legend)

        self.normalise = None
        self.options = options
        self.set_data_type(PDSData)
        self.set_processor_type(PDSDataProcessor)

    def set_options(self, normalise: bool = None, *args, **kwargs):
        self.normalise = normalise

    def plot(self, title, legend):
        """
        Show the absorbance spectrum
        """
        plotter = ScatterDataPlotter(title, "wavelength", "signal")
        plotter.ready_plot(self.data_processors, legend)
        plotter.draw_plot()
