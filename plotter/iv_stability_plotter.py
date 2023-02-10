from data.data_processors.iv_stability_dataprocessor import IVStabilityDataProcessor
from utils.plot_preppers.four_subplots_prepper import four_subplots_prepper
from plotter.plotter import Plotter
import plotly.graph_objects as go
import plotly.express as px


class IVStabilityPlotter(Plotter):
    def __init__(self, title):
        self.title = title
        self.iv_stability_processors = None
        self.fig = None
        self.colours = None

    def ready_plot(self, iv_stability_processors: dict[str, IVStabilityDataProcessor], legend_title: str):
        self.fig = four_subplots_prepper()
        self.colours = px.colors.qualitative.Plotly
        self.fig.update_layout(
            title={'text': self.title},
            legend_title=legend_title,
        )
        self.iv_stability_processors = iv_stability_processors

    def draw_plot(self):
        # Grab the values for Isc, Voc, FF and eff from the data
        for label in self.iv_stability_processors:
            currents = self.iv_stability_processors[label].get_data('isc')
            voltages = self.iv_stability_processors[label].get_data('voc')
            fill_factors = self.iv_stability_processors[label].get_data('fill_factor')
            max_powers = self.iv_stability_processors[label].get_data('mpp_power')
            times = [i for i in range(len(currents))]

            self.fig.add_trace(
                go.Scatter(
                    x=times,
                    y=currents,
                    legendgroup=label,
                    name=label,
                    # marker=dict(color=self.colours[index % len(self.colours)])
                ),
                row=1, col=1
            )
            self.fig.add_trace(
                go.Scatter(
                    x=times,
                    y=voltages,
                    legendgroup=label,
                    name=label,
                    showlegend=False,
                    # marker=dict(color=self.colours[index % len(self.colours)])
                ),
                row=1, col=2
            )
            self.fig.add_trace(
                go.Scatter(
                    x=times,
                    y=fill_factors,
                    legendgroup=label,
                    name=label,
                    showlegend=False,
                    # marker=dict(color=self.colours[index % len(self.colours)])
                ),
                row=2, col=1
            )
            self.fig.add_trace(
                go.Scatter(
                    x=times,
                    y=max_powers,
                    legendgroup=label,
                    name=label,
                    showlegend=False,
                    # marker=dict(color=self.colours[index % len(self.colours)])
                ),
                row=2, col=2
            )
        self.fig.show()
