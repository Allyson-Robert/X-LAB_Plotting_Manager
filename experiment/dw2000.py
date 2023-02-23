from data.data_processors.scatter_data.absorbance_data_processor import AbsorbanceScatterDataProcessor
from data.datatypes.scatter_data.absorbance_scatter import AbsorbanceScatterData
from plotter.scatter_data_plotter import ScatterDataPlotter
from experiment.experiment_worker import ExperimentWorker
from fileset.fileset import Fileset
from PyQt5 import QtCore


class DW2000(ExperimentWorker):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(int)

    def __init__(self,  device, fileset, plot_type, legend):
        # super() delegates method calls to a parent
        super(DW2000, self).__init__()

        self.device = device
        self.fileset = fileset
        self.plot_type = plot_type
        self.legend = legend

        self.absorbance_processor = None

    def run(self):
        # Set the data
        self.set_data(self.fileset)

        # Grab the correct plot and execute it
        plot_type = getattr(self, self.plot_type)
        plot_type(title=self.fileset.get_name(), legend=self.legend)

    def set_data(self,  fileset: Fileset):
        assert fileset.get_structure_type() == "flat"

        filepaths = fileset.get_filepaths()
        self.absorbance_processor = {}
        for key in filepaths:
            data = AbsorbanceScatterData(key)
            data.read_file(filepaths[key])
            self.absorbance_processor[key] = AbsorbanceScatterDataProcessor(data)

    def normal_plot(self, title, legend):
        plotter = ScatterDataPlotter(title, "wavelength", "absorbance")
        plotter.ready_plot(self.absorbance_processor, legend)
        plotter.draw_plot()

    def rainbow_plot(self, title, legend):
        # TODO: Add a rainbow plotting thing for a single file
        raise NotImplementedError
