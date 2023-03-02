from data.data_processors.data_processors import DataProcessor
from utils.plot_preppers.scatter_prep import scatter_prepper
from plotter.plotter import Plotter
import plotly.graph_objects as go


class HistogramPlotter(Plotter):
    def __init__(self, title, observable: str):
        self.title = title
        self.fig = go.Figure()
        self.observable = observable

        self.data_processors = None

    def ready_plot(self, data_processors: dict[str, DataProcessor], legend_title: str):
        self.fig = scatter_prepper(self.fig)
        self.fig.update_layout(
            title={'text': self.title},
            legend_title=legend_title,
        )
        self.data_processors = data_processors

    def draw_plot(self):
        for lbl in self.data_processors:
            processor = self.data_processors[lbl]

            self.fig.add_trace(
                go.Histogram(x=processor.get_data(self.observable))
            )

        # Grab axis titles from last IVData
        self.fig.update_layout(
            xaxis_title=processor.get_units(self.observable),
            yaxis_title="$Counts$",
        )
        self.fig.show()
