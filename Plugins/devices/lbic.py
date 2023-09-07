from plugins.data.data_processors.lbic_image_processor import LBICImageProcessor
from plugins.devices.device_worker import DeviceWorkerCore
from plugins.data.data_types import LBICImage
from plugins import plotter as plt


class LBIC(DeviceWorkerCore):
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
            self.profile_position = profile_position / 1000 # gui set to mm
        self.lower_bound = lower_bound / 1000000 # gui set to uA, no clue how to set this in the spinbox itself
        self.upper_bound = upper_bound / 1000000 # gui set to uA

    def plot_image(self, title, legend):
        """
        Heatmap/Image plot of the measured intensities at each position
        """
        plotter = plt.HeatmapPlotter(title)
        plotter.ready_plot(self.data_processors, legend)
        plotter.set_options(zrange=[self.lower_bound, self.upper_bound], profiles=self.enable_profiles)
        plotter.draw_plot()

    def plot_3d(self, title, legend):
        """
        Surface plot of the measured intensities at each position
        """
        plotter = plt.SurfacePlotter(title)
        plotter.ready_plot(self.data_processors, legend)
        plotter.set_options(zrange=[self.lower_bound, self.upper_bound])
        plotter.draw_plot()

    def plot_intensities(self, title, legend):
        """
        Scatter plot of all measured intensities
        """
        plotter = plt.HistogramPlotter(title, "current_list")
        plotter.ready_plot(self.data_processors, legend)
        plotter.draw_plot()

    def plot_horiz_profile(self, title, legend):
        """
        Scatter plot of the measured intensities along a horizontal profile
        """
        plotter = plt.ScatterDataPlotter(title, "x_axis", "horizontal_profile")
        plotter.ready_plot(self.data_processors, legend)
        plotter.draw_plot(y_position=self.profile_position)

    def plot_vert_profile(self, title, legend):
        """
        Scatter plot of the measured intensities along a vertical profile
        """
        raise NotImplementedError

    def plot_diagonal_profile(self, title, legend):
        """
        Scatter plot of the measured intensities along a diagonal profile.
        """
        raise NotImplementedError


