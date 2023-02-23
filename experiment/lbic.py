from experiment.experiment_worker import ExperimentWorkerCore
from fileset.fileset import Fileset


class LBIC(ExperimentWorkerCore):
    def __init__(self,  device, fileset, plot_type, legend):
        # super() delegates method calls to a parent
        super(LBIC, self).__init__()

        self.device = device
        self.fileset = fileset
        self.plot_type = plot_type
        self.legend = legend

        self.iv_stability_processors = None

    def set_data(self,  fileset: Fileset):
        raise NotImplementedError

    def show_image(self):
        """
        Heatmap/Image plot of the measured intensities at each position
        """
        raise NotImplementedError

    def show_3d(self):
        """
        Surface plot of the measured intensities at each position
        """
        raise NotImplementedError

    def plot_intensities(self):
        """
        Scatter plot of all measured intensities
        """
        raise NotImplementedError

    def plot_horiz_profile(self):
        """
        Scatter plot of the measured intensities along a horizontal profile
        """
        raise NotImplementedError

    def plot_vert_profile(self):
        """
        Scatter plot of the measured intensities along a vertical profile
        """
        raise NotImplementedError


