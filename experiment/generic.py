from experiment.experiment_worker import ExperimentWorker
from fileset.fileset import Fileset
from PyQt5 import QtCore


class Generic(ExperimentWorker):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(int)

    def __init__(self,  device, fileset, plot_type, legend):
        # super() delegates method calls to a parent
        super(Generic, self).__init__()

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
        raise NotImplementedError

    def plot(self):
        """
        Show the scatter plot
        """
        raise NotImplementedError

    def plot_distribution(self):
        """
        Show a histogram
        """
        raise NotImplementedError