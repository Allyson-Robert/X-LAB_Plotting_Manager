from experiment.experiment_worker import ExperimentWorkerCore
from fileset.fileset import Fileset


class PDS(ExperimentWorkerCore):
    def __init__(self,  device, fileset, plot_type, legend):
        # super() delegates method calls to a parent
        super(PDS, self).__init__()

        self.device = device
        self.fileset = fileset
        self.plot_type = plot_type
        self.legend = legend

        self.iv_stability_processors = None

    def set_data(self,  fileset: Fileset):
        raise NotImplementedError

    def plot(self):
        """
        Show the absorbance spectrum
        """
        raise NotImplementedError
