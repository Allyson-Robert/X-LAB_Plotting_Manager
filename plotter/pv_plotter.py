from plotter.plotter import Plotter
from data.collections.scatter_collections.scatter_collection import ScatterCollection
import plotly.graph_objects as go
from utils.plot_preppers.scatter_prep import scatter_prepper


class PVPlotter(Plotter):
    def __init__(self, title, legend_title):
        self.title = title
        self.legend_title = legend_title
        self.fig = go.Figure()

    def ready_plot(self):
        self.fig = scatter_prepper(self.fig)
        self.fig.update_layout(
            title={'text': self.title},
            legend_title=self.legend_title,
        )

        self.fig.update_layout(
            xaxis_title="Voltage (V)",
            yaxis_title="Power (A)",
        )

    def draw_plot(self, collection: ScatterCollection):
        data = collection.get_data()
        for lbl in data:
            iv_scatter = data[lbl]
            iv_scatter.get_data('power')
            self.fig.add_trace(go.Scatter(
                x=iv_scatter.get_data('voltage'),
                y=iv_scatter.get_data('power'),
                mode='lines',
                name=iv_scatter.get_data('label')
            ))
        self.fig.show()
