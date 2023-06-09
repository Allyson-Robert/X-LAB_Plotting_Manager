from data.data_processors.data_processors import DataProcessor
from utils.plot_preppers.scatter_prep import scatter_prepper
from utils.plot_preppers.export_to_svg import get_svg_config
from plotter.plotter import Plotter
import plotly.graph_objects as go


class ScatterDataPlotter(Plotter):
    def __init__(self, title, x_observable: str, y_observable: str):
        self.title = title
        self.fig = go.Figure()
        self.x_observable = x_observable
        self.y_observable = y_observable

        self.data_processors = None

        self.titles_set = False

    def ready_plot(self, data_processors: dict[str, DataProcessor], legend_title: str):
        self.fig = scatter_prepper(self.fig)
        self.fig.update_layout(
            title={'text': self.title},
            legend_title=legend_title,
        )
        self.data_processors = data_processors

    def set_axes_titles(self, x_title, y_title):
        self.fig.update_layout(
            xaxis_title=x_title,
            yaxis_title=y_title,
        )
        self.titles_set = True

    def draw_plot(self, presentation: bool, *args, **kwargs):
        if presentation:
            line = go.Scatter.Line(width=5)
        else:
            line = None

        # FEATURE REQUEST: Draw plots with errors
        for lbl in self.data_processors:
            scatter = self.data_processors[lbl]
            self.fig.add_trace(go.Scatter(
                x=scatter.get_data(self.x_observable, *args, **kwargs),
                y=scatter.get_data(self.y_observable, *args, **kwargs),
                mode='lines',
                name=scatter.get_data('label'),
                line=line
            ))
        # Grab axis titles from last IVData if they have not yet been externally set
        if not self.titles_set:
            self.set_axes_titles(
                scatter.get_units(self.x_observable),
                scatter.get_units(self.y_observable)
            )
        self.fig.show(config=get_svg_config())
