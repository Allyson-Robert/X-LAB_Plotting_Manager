from plugins.data.data_processors.data_processors import DataProcessor
from utils.plot_preppers.heatmap_prepper import heatmap_prepper, add_profiles
from utils.plot_preppers.export_to_svg import get_svg_config
from plugins.plotter.plotter import Plotter
import plotly.graph_objects as go


class HeatmapPlotter(Plotter):
    def __init__(self, title):
        self.color = None
        self.zauto = None
        self.zrange = None

        self.title = title
        self.image_processor = None
        self.fig = go.Figure()

    def ready_plot(self, processor: DataProcessor, legend_title: str):
        self.fig = heatmap_prepper(self.fig)
        self.fig.update_layout(
            title={'text': self.title},
            legend_title=legend_title,
        )
        if len(processor) == 1:
            self.image_processor = processor
        else:
            raise ValueError("Too many images requested")

    def set_options(self, zrange: list = None, color: str = 'turbid', profiles: bool = None):
        # Set range
        if zrange is None:
            self.zrange = [0, 0]
            self.zauto = True
        else:
            self.zrange = zrange
            self.zauto = False

        # Set colour
        self.color = color

        # Add profiles if requested
        if profiles:
            add_profiles(self.fig)

    def draw_plot(self):
        key = list(self.image_processor.keys())[0]
        processor = self.image_processor[key]
        self.fig.update_layout(yaxis_title=processor.get_units("y_axis"))
        self.fig.add_trace(
            go.Heatmap(
                x=processor.get_data("x_axis"),
                y=processor.get_data("y_axis"),
                z=processor.get_data("current"),
                zauto=self.zauto,
                zmin=self.zrange[0],
                zmax=self.zrange[1],
                colorscale="turbid",
                reversescale=True,
                colorbar=dict(title=processor.get_units("current")),
                # hovertemplate won't work with units as currently defined
                hovertemplate='x (mm): %{x}<br>y (mm): %{y}<br>I (A): %{z}<extra></extra>'
            )
        )
        self.fig.show(config=get_svg_config())
