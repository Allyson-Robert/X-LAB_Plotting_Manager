from plotter.plotter import Plotter
from data.collections.scatter_collections.iv_scatter_collection import IVScatterCollection
import plotly.graph_objects as go
from utils.plot_preppers.scatter_prep import scatter_prepper


class IVScatterDataPlotter(Plotter):
    def __init__(self, title, x_observable: str, y_observable: str):
        self.title = title
        self.fig = go.Figure()
        self.x_observable = x_observable
        self.y_observable = y_observable

        self.collection = None

    def ready_plot(self, collection: IVScatterCollection, legend_title: str):
        self.fig = scatter_prepper(self.fig)
        self.fig.update_layout(
            title={'text': self.title},
            legend_title=legend_title,
        )
        self.collection = collection

    def draw_plot(self):
        data = self.collection.get_data()
        for lbl in data:
            iv_scatter = data[lbl]
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
