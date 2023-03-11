from data.data_processors.lbic_image_processor import LBICImageProcessor
from experiment.experiment_worker import ExperimentWorkerCore
from data.datatypes.lbic_image import LBICImage
from plotter.heatmap_plotter import HeatmapPlotter


class LBIC(ExperimentWorkerCore):
    def __init__(self, device, fileset, plot_type, legend, options):
        # super() delegates method calls to a parent
        super().__init__(device, fileset, plot_type, legend)

        self.upper_bound = None
        self.lower_bound = None
        self.profile_position = None
        self.enable_profiles = None

        self.options = options

        self.iv_stability_processors = None
        self.set_data_type(LBICImage)
        self.set_processor_type(LBICImageProcessor)

    def set_options(self, enable_profiles: bool, profile_position: float, lower_bound: float, upper_bound: float,
                    *args, **kwargs):
        self.enable_profiles = enable_profiles
        if enable_profiles:
            self.profile_position = profile_position / 1000 # GUI set to mm
        self.lower_bound = lower_bound / 1000000 # GUI set to uA, no clue how to set this in the spinbox itself
        self.upper_bound = upper_bound / 1000000 # GUI set to uA

    def plot_image(self, title, legend):
        """
        Heatmap/Image plot of the measured intensities at each position
        """
        plotter = HeatmapPlotter(title)
        plotter.ready_plot(self.data_processors, legend)
        plotter.set_options(zrange=[self.lower_bound, self.upper_bound], profiles=self.enable_profiles)
        plotter.draw_plot()

    def plot_3d(self):
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


