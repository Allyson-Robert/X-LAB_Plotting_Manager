from data.data_processors.scatter_data.iv_stability_data_processor import IVStabilityDataProcessor
from utils.plot_preppers.four_subplots_prepper import four_subplots_prepper
from utils.plot_preppers.export_to_svg import get_svg_config
from plotter.plotter import Plotter
import plotly.graph_objects as go
import plotly.express as px
from utils.export_to_csv import export_to_csv


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

    def draw_plot(self, export):
        # Grab the values for Isc, Voc, FF and eff from the data
        counter = 0
        for label in self.iv_stability_processors:
            self.iv_stability_processors[label].validate_observables('isc', 'voc', 'fill_factor', 'mpp_power')
            currents = self.iv_stability_processors[label].get_data('isc')
            voltages = self.iv_stability_processors[label].get_data('voc')
            fill_factors = self.iv_stability_processors[label].get_data('fill_factor')
            max_powers = self.iv_stability_processors[label].get_data('mpp_power')
            times = self.iv_stability_processors[label].get_data('time_differences')

            self.fig.add_trace(
                go.Scatter(
                    x=times,
                    y=currents,
                    legendgroup=label,
                    name=label,
                    marker=dict(color=self.colours[counter % len(self.colours)])
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
                    marker=dict(color=self.colours[counter % len(self.colours)])
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
                    marker=dict(color=self.colours[counter % len(self.colours)])
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
                    marker=dict(color=self.colours[counter % len(self.colours)])
                ),
                row=2, col=2
            )
            counter += 1
            if export:
                # TODO: Get filename from GUI
                export_to_csv(filename=f"temp{counter}.csv", list_of_lists=[times, currents, voltages, fill_factors,
                                                                            max_powers])

        self.fig.show(config=get_svg_config())
