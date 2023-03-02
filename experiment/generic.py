from data.data_processors.scatter_data.scatter_data_processor import ScatterDataProcessor
from data.datatypes.scatter_data.generic_scatter import GenericData
from experiment.experiment_worker import ExperimentWorkerCore
from plotter.scatter_data_plotter import ScatterDataPlotter
from plotter.histogram_plotter import HistogramPlotter
from fileset.fileset import Fileset


class Generic(ExperimentWorkerCore):
    def __init__(self,  device, fileset, plot_type, legend):
        # super() delegates method calls to a parent
        super(Generic, self).__init__()

        self.device = device
        self.fileset = fileset
        self.plot_type = plot_type
        self.legend = legend

        self.data_processor = None

    def set_data(self,  fileset: Fileset):
        assert fileset.get_structure_type() == "flat"

        # Initialise an empty dict and get the required filepaths
        self.data_processor = {}
        filepaths = fileset.get_filepaths()

        # Progress housekeeping
        nr_of_files = len(filepaths)
        counter = 0

        # Read the data and instantiate a processor for each file
        for key in filepaths:
            # TODO: Should there be a different processor for each type of file? Answer: no, should get label from GUI
            data = GenericData(key)
            data.read_file(filepaths[key])
            self.data_processor[key] = ScatterDataProcessor(data)

            # Emit progress signal
            self.progress.emit(int(100*counter/nr_of_files))
            counter += 1

    def plot(self, title, legend):
        """
        Show the scatter plot
        """
        # TODO: Bodge for quick plot, grab quantities from GUI
        plotter = ScatterDataPlotter(title, "independent", "dependent")
        plotter.ready_plot(self.data_processor, legend)
        plotter.draw_plot()

    def plot_distribution(self, title, legend):
        """
        Show a histogram
        """
        plotter = HistogramPlotter(title, "dependent")
        plotter.ready_plot(self.data_processor, legend)
        plotter.draw_plot()