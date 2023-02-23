from data.data_processors.scatter_data.iv_stability_data_processor import IVStabilityDataProcessor
from data.datatypes.scatter_data.iv_scatter import IVScatterData
from plotter.iv_stability_plotter import IVStabilityPlotter
from experiment.experiment_worker import ExperimentWorker
from fileset.fileset import Fileset
from PyQt5 import QtCore


class Stability(ExperimentWorker):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(int)

    def __init__(self,  device, fileset, plot_type, legend):
        # super() delegates method calls to a parent
        super(Stability, self).__init__()

        self.device = device
        self.fileset = fileset
        self.plot_type = plot_type
        self.legend = legend

        self.iv_stability_processors = None

    def run(self):
        # Set the data
        self.set_data(self.fileset)

        # Grab the correct plot and execute it
        plot_type = getattr(self, self.plot_type)
        plot_type(title=self.fileset.get_name(), legend=self.legend)

    def set_data(self, fileset: Fileset):
        assert fileset.get_structure_type() == "structured"

        filepaths = fileset.get_filepaths()
        start_date = fileset.get_experiment_date()
        self.iv_stability_processors = {}
        for solar_cell in filepaths:
            processors_list = []
            for iv_curve in filepaths[solar_cell]:
                iv_data = IVScatterData(iv_curve)
                iv_data.read_file(filepaths[solar_cell][iv_curve])
                processors_list.append(iv_data)
            self.iv_stability_processors[solar_cell] = IVStabilityDataProcessor(processors_list, start_date)

    def plot_four(self, title, legend):
        plotter = IVStabilityPlotter(title)
        plotter.ready_plot(self.iv_stability_processors, legend)
        plotter.draw_plot()
