from data.data_processors.scatter_data.scatter_data_processor import ScatterDataProcessor
from data.datatypes.scatter_data.generic_scatter import GenericScatterData
from experiment.experiment_worker import ExperimentWorkerCore
import plotter as plt


class Generic(ExperimentWorkerCore):

    def __init__(self, device, fileset, plot_type, legend, options):
        # super() delegates method calls to a parent
        super().__init__(device, fileset, plot_type, legend)

        self.x_title = None
        self.y_title = None
        self.legend_title = None
        self.options = options
        self.data_processors = None

        self.set_data_type(GenericScatterData)
        self.set_processor_type(ScatterDataProcessor)

    def set_options(self, x_title: str, y_title: str, legend_title: str, *args, **kwargs):
        self.x_title = x_title
        self.y_title = y_title
        self.legend_title = legend_title

    def plot(self, title, legend):
        """
        Show the scatter plot
        """
        plotter = plt.ScatterDataPlotter(title, "independent", "dependent")
        plotter.ready_plot(self.data_processors, self.legend_title)
        plotter.set_axes_titles(self.x_title, self.y_title)
        plotter.draw_plot()

    def plot_distribution(self, title, legend):
        """
        Show a histogram
        """
        plotter = plt.HistogramPlotter(title, "dependent")
        plotter.ready_plot(self.data_processors, self.legend_title)
        plotter.set_axes_titles(self.y_title)
        plotter.draw_plot()