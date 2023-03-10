from data.data_processors.scatter_data.fluorescence_data_processor import FluorescenceScatterDataProcessor
from data.datatypes.scatter_data.fluorescence_scatter import FluorescenceData
from experiment.experiment_worker import ExperimentWorkerCore
from plotter.scatter_data_plotter import ScatterDataPlotter
from fileset.fileset import Fileset


class PTI(ExperimentWorkerCore):
    def __init__(self,  device, fileset, plot_type, legend):
        # super() delegates method calls to a parent
        super(PTI, self).__init__()

        self.device = device
        self.fileset = fileset
        self.plot_type = plot_type
        self.legend = legend

        self.fluo_data_processor = None

    def set_data(self,  fileset: Fileset):
        assert fileset.get_structure_type() == "flat"

        filepaths = fileset.get_filepaths()
        self.fluo_data_processor = {}
        for key in filepaths:
            fluo_data = FluorescenceData(key)
            fluo_data.read_file(filepaths[key])
            self.fluo_data_processor[key] = FluorescenceScatterDataProcessor(fluo_data)

    def plot(self, title, legend):
        """
        Show the fluorescence spectrum
        """
        plotter = ScatterDataPlotter(title, "wavelength", "fluorescence")
        plotter.ready_plot(self.fluo_data_processor, legend)
        plotter.draw_plot()
