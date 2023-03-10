from data.data_processors.data_processors import DataProcessor
from utils.plot_preppers.heatmap_prepper import heatmap_prep
from plotter.plotter import Plotter
import plotly.graph_objects as go


class HeatmapPlotter(Plotter):
    def __init__(self, title):
        self.title = title
        self.image_processors = None
        self.fig = go.Figure()

    def ready_plot(self, processors: DataProcessor, legend_title: str):
        self.fig = heatmap_prep(self.fig)

    def draw_plot(self):
        pass
