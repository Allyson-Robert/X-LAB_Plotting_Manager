from experiment.experiment_worker import ExperimentWorker
from utils.experiment_worker.set_data import set_data
from fileset.fileset import Fileset
from PyQt5 import QtCore


class PTI(ExperimentWorker):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(int)

    def __init__(self,  device, fileset, plot_type, legend):
        # super() delegates method calls to a parent
        super(PTI, self).__init__()

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

    def set_data(self,  fileset: Fileset):
        self.fluo_data_processor = set_data(fileset, )
        assert fileset.get_structure_type() == "flat"

        filepaths = fileset.get_filepaths()
        self.fluo_data_processor = {}
        for key in filepaths:
            fluo_data = IVScatterData(key)
            fluo_data.read_file(filepaths[key])
            self.fluo_data_processor[key] = IVScatterDataProcessor(iv_data)

    def plot(self):
        """
        Show the fluorescence spectrum
        """
        raise NotImplementedError