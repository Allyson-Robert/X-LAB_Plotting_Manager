from plugins.data.data_processors.data_processors import DataProcessor
from utils.plot_preppers.surface_prepper import surface_prepper
from utils.plot_preppers.export_to_svg import get_svg_config
from plugins.plotter.plotter import Plotter
import plotly.graph_objects as go


class SurfacePlotter(Plotter):
    def __init__(self, title):
        self.zrange = None
        self.color = None
        self.title = title
        self.fig = go.Figure()

        self.data_processors = None

    def ready_plot(self, processor: DataProcessor, legend_title: str):
        self.fig = surface_prepper(self.fig) # Currently this does nothing
        self.fig.update_layout(
            title={'text': self.title},
            legend_title=legend_title,
        )
        if len(processor) == 1:
            self.data_processors = processor
        else:
            raise ValueError("Too many images requested")

    def set_options(self, zrange: list = None, color: str = 'turbid'):
        # Set range
        if zrange is None:
            self.zrange = [min(self.z), max(self.z)]
        else:
            self.zrange = zrange

        # Set colour
        self.color = color

    def draw_plot(self):
        # Get only processor
        key = list(self.data_processors.keys())[0]
        processor = self.data_processors[key]

        # Generate image as heatmap including the colorscale
        self.fig.add_trace(
            go.Surface(
                x=processor.get_data("x_axis"),
                y=processor.get_data("y_axis"),
                z=processor.get_data("current"),
                cmin=self.zrange[0],
                cmax=self.zrange[1],
                colorscale=self.color,
                reversescale=True,
                colorbar=dict(title=processor.get_units("current")),
                hovertemplate='x (mm): %{x}<br>y (mm): %{y}<br>I (A): %{z}<extra></extra>'
            )
        )

        self.fig.update_layout(
            scene=dict(
                zaxis=dict(range=self.zrange),
            ),
        )
        self.fig.show(config=get_svg_config())
