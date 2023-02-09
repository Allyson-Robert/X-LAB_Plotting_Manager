import plotly.express as px
import plotly.graph_objects as go
from plotter.plotter import Plotter
from data.collections.scatter_collections.iv_structured_collection import IVStructuredCollection
from utils.plot_preppers.four_subplots_prepper import four_subplots_prepper


class IVStabilityPlotter(Plotter):
    def __init__(self, title):
        self.title = title
        self.collection = None
        self.fig = None
        self.colours = None

    def ready_plot(self, collection: IVStructuredCollection, legend_title: str):
        self.fig = four_subplots_prepper()
        self.colours = px.colors.qualitative.Plotly
        self.fig.update_layout(
            title={'text': self.title},
            legend_title=legend_title,
        )
        self.collection = collection

    def draw_plot(self):
        data = self.collection.get_data()
        # Grab the values for Isc, Voc, FF and eff from the data
        currents = {}
        voltages = {}
        fills = {}
        max_power = {}
        times = {}
        for index, series in enumerate(data):
            currents[series] = []
            voltages[series] = []
            fills[series] = []
            max_power[series] = []
            times[series] = [0]
            for point in data[series]:
                iv_data = data[series][point]
                currents[series].append(iv_data.get_data("isc"))
                voltages[series].append(iv_data.get_data("voc"))
                fills[series].append(iv_data.get_data("fill_factor"))
                max_power[series].append(iv_data.get_data("mpp_power"))
                times[series].append(times[series][-1]+1)

            self.fig.add_trace(
                go.Scatter(
                    x=times[series],
                    y=currents[series],
                    legendgroup=series,
                    name=series,
                    marker=dict(color=self.colours[index % len(self.colours)])
                ),
                row=1, col=1
            )
            self.fig.add_trace(
                go.Scatter(
                    x=times[series],
                    y=voltages[series],
                    legendgroup=series,
                    name=series,
                    showlegend=False,
                    marker=dict(color=self.colours[index % len(self.colours)])
                ),
                row=1, col=2
            )
            self.fig.add_trace(
                go.Scatter(
                    x=times[series],
                    y=fills[series],
                    legendgroup=series,
                    name=series,
                    showlegend=False,
                    marker=dict(color=self.colours[index % len(self.colours)])
                ),
                row=2, col=1
            )
            self.fig.add_trace(
                go.Scatter(
                    x=times[series],
                    y=max_power[series],
                    legendgroup=series,
                    name=series,
                    showlegend=False,
                    marker=dict(color=self.colours[index % len(self.colours)])
                ),
                row=2, col=2
            )
        self.fig.show()
