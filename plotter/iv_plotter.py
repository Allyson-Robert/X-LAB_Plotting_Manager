from data.data_processors.iv_data_processor import IVScatterDataProcessor
from utils.plot_preppers.scatter_prep import scatter_prepper
from plotter.plotter import Plotter
import plotly.graph_objects as go


class IVScatterDataPlotter(Plotter):
    def __init__(self, title, x_observable: str, y_observable: str):
        self.title = title
        self.fig = go.Figure()
        self.x_observable = x_observable
        self.y_observable = y_observable

        self.iv_data_processors = None

    def ready_plot(self, iv_data_processors: dict[str, IVScatterDataProcessor], legend_title: str):
        self.fig = scatter_prepper(self.fig)
        self.fig.update_layout(
            title={'text': self.title},
            legend_title=legend_title,
        )
        self.iv_data_processors = iv_data_processors

    def draw_plot(self):
        for lbl in self.iv_data_processors:
            iv_scatter = self.iv_data_processors[lbl]
            self.fig.add_trace(go.Scatter(
                x=iv_scatter.get_data(self.x_observable),
                y=iv_scatter.get_data(self.y_observable),
                mode='lines',
                name=iv_scatter.get_data('label')
            ))
        # Grab axis titles from last IVScatterData
        self.fig.update_layout(
            xaxis_title=iv_scatter.get_units(self.x_observable),
            yaxis_title=iv_scatter.get_units(self.y_observable),
        )
        self.fig.show()
