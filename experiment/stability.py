from data.data_processors.scatter_data.iv_stability_data_processor import IVStabilityDataProcessor
from data.datatypes.scatter_data.iv_scatter import IVData
from experiment.experiment_worker import ExperimentWorkerCore
from plotter.iv_stability_plotter import IVStabilityPlotter
from fileset.fileset import Fileset


class Stability(ExperimentWorkerCore):
    def __init__(self, device, fileset, plot_type, legend, options):
        # super() delegates method calls to a parent
        super().__init__(device, fileset, plot_type, legend)

        self.cell_area = None
        self.relative = None
        self.log_time = None
        self.export = None
        self.options = options

        self.iv_stability_processors = None

    def set_options(self, export: bool, log_time: bool, relative: bool, cell_area: float, *args, **kwargs):
        self.export = export
        self.log_time = log_time
        self.relative = relative
        self.cell_area = cell_area

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
        plotter.draw_plot(export=self.export, log_time=self.log_time, relative=self.relative, cell_area=self.cell_area)

    def plot_isc(self, title, legend):
        raise NotImplementedError

    def plot_jsc(self, title, legend):
        raise NotImplementedError

    def plot_voc(self, title, legend):
        raise NotImplementedError

    def plot_ff(self, title, legend):
        raise NotImplementedError

    def plot_mpp(self, title, legend):
        raise NotImplementedError

    def plot_isc_voc_scatte(self, title, legend):
        raise NotImplementedError

    def plot_eff(self, title, legend):
        raise NotImplementedError
