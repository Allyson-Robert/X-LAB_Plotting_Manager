from data.data_processors.scatter_data.iv_stability_data_processor import IVStabilityDataProcessor
from data.datatypes.scatter_data.iv_scatter import IVData
from experiment.experiment_worker import ExperimentWorkerCore
from plotter.iv_stability_plotter import IVStabilityPlotter
from fileset.fileset import Fileset


class Stability(ExperimentWorkerCore):
    def __init__(self,  device, fileset, plot_type, legend, options):
        # super() delegates method calls to a parent
        super(Stability, self).__init__()

        self.export = None
        self.device = device
        self.fileset = fileset
        self.plot_type = plot_type
        self.legend = legend
        self.options = options

        self.iv_stability_processors = None

    def set_options(self, export: bool, *args, **kwargs):
        self.export = export

    def set_data(self, fileset: Fileset):
        assert fileset.get_structure_type() == "structured"

        # Initialise an empty dict and get the required filepaths
        filepaths = fileset.get_filepaths()
        start_date = fileset.get_experiment_date()
        self.iv_stability_processors = {}

        # Progress housekeeping
        nr_of_files = len(filepaths)
        counter = 0

        # Read the data and instantiate a processor for each cell
        for solar_cell in filepaths:
            processors_list = []
            for iv_curve in filepaths[solar_cell]:
                iv_data = IVData(iv_curve)
                iv_data.read_file(filepaths[solar_cell][iv_curve])
                processors_list.append(iv_data)

            self.iv_stability_processors[solar_cell] = IVStabilityDataProcessor(processors_list, start_date)

            # Emit progress signal
            counter += 1
            self.progress.emit(int(100*counter/nr_of_files))

    def plot_four(self, title, legend):
        plotter = IVStabilityPlotter(title)
        plotter.ready_plot(self.iv_stability_processors, legend)
        plotter.draw_plot(export=self.export)
        # if self.export:
        #     plotter.export()
