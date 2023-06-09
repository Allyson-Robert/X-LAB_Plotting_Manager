from data.data_processors.scatter_data.absorbance_data_processor import AbsorbanceScatterDataProcessor
from data.datatypes.scatter_data.absorbance_scatter import AbsorbanceData
from experiment.experiment_worker import ExperimentWorkerCore
from plotter.scatter_data_plotter import ScatterDataPlotter
from fileset.fileset import Fileset
from PyQt5 import QtCore


class DW2000(ExperimentWorkerCore):
    def __init__(self, device, fileset, plot_type, legend, options):
        # super() delegates method calls to a parent
        super().__init__(device, fileset, plot_type, legend)

        self.presentation = None
        self.options = options
        self.set_data_type(AbsorbanceData)
        self.set_processor_type(AbsorbanceScatterDataProcessor)

    def set_options(self, presentation: bool, *args, **kwargs):
        self.presentation = presentation

    def normal_plot(self, title, legend):
        plotter = ScatterDataPlotter(title, "wavelength", "absorbance")
        plotter.ready_plot(self.data_processors, legend)
        plotter.draw_plot(presentation=self.presentation)

    def rainbow_plot(self, title, legend):
        # FEATURE REQUEST: Add a rainbow plotting thing for a single file
        raise NotImplementedError
