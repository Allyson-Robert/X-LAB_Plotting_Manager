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

    def ready_plot(self, iv_stability_processors: dict[str, IVStabilityDataProcessor], legend_title: str, colours: dict):
        self.fig = four_subplots_prepper(subplots_titles=("Short-Circuit Current", "Open Circuit Voltage", "Fill Factor", "Maximum Power"))

        self.fig.update_layout(
            title={'text': self.title},
            legend_title=legend_title,
        )
        self.iv_stability_processors = iv_stability_processors

        # Trying to allow the colours to be manually set
        if colours is None:
            self.colours = {}
            counter = 0
            for label in self.iv_stability_processors:
                self.colours[label] = px.colors.qualitative.Plotly[counter % len(px.colors.qualitative.Plotly)]
                counter += 1
        else:
            self.colours = colours
        print(self.colours)

    def draw_plot(self, export: bool, relative: bool, log_time: bool, cell_area: float = 0.0):
        # Grab the values for Isc, Voc, FF and eff from the data
        counter = 0
        for label in self.iv_stability_processors:
            self.iv_stability_processors[label].validate_observables('isc', 'voc', 'fill_factor', 'mpp_power')
            currents = self.iv_stability_processors[label].get_data('isc')
            voltages = self.iv_stability_processors[label].get_data('voc')
            fill_factors = self.iv_stability_processors[label].get_data('fill_factor')
            max_powers = self.iv_stability_processors[label].get_data('mpp_power')
            times = self.iv_stability_processors[label].get_data('time_differences')

            if cell_area != 0.0:
                currents = [c / (cell_area / 100) for c in currents]
                max_powers = [mpp / (cell_area / 100) for mpp in max_powers]
                self.fig['layout']['yaxis']['title'] = '$I_{sc} ~(A / cm^2)$'
                self.fig['layout']['yaxis4']['title'] = '$P_{max} ~(W / cm^2)$'

            if relative:
                currents = [c/currents[0] for c in currents]
                voltages = [v/voltages[0] for v in voltages]
                fill_factors = [ff/fill_factors[0] for ff in fill_factors]
                max_powers = [mpp/max_powers[0] for mpp in max_powers]
                self.fig['layout']['yaxis']['title'] = '$I_{sc}/I_{sc, 0} ~(dimensionless)$'
                self.fig['layout']['yaxis2']['title'] = '$V_{oc}/V_{oc, 0} ~(dimensionless)$'
                self.fig['layout']['yaxis3']['title'] = '$Rel. Fill~factor ~(dimensionless)$'
                self.fig['layout']['yaxis4']['title'] = '$P_{max}/P_{max, 0} ~(dimensionless)$'

            self.fig.add_trace(
                go.Scatter(
                    x=times,
                    y=currents,
                    legendgroup=label,
                    name=label,
                    marker=dict(color=self.colours[label])
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
                    marker=dict(color=self.colours[label])
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
                    marker=dict(color=self.colours[label])
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
                    marker=dict(color=self.colours[label])
                ),
                row=2, col=2
            )
            self.fig.update_layout(margin=dict(l=0, r=0, t=50, b=0),
                              xaxis=dict(title=dict(standoff=10)),
                              yaxis=dict(title=dict(standoff=10)))
            counter += 1
            if export:
                # GUI FEATURE REQUEST: Get filename from GUI
                # FEATURE REQUEST: Filename might be useful
                export_to_csv(
                    filename=f"position_{counter}_stability.csv",
                    list_of_lists=[times, currents, voltages, fill_factors, max_powers],
                    header=["time (hrs)", "current (A)", "voltage (V)", "Fill factor (a.u.)", "Max power (W)"]
                )
            if log_time:
                for i in range(1, 3):
                    for j in range(1, 3):
                        self.fig.update_xaxes(type="log", row=i, col=j)

        self.fig.show(config=get_svg_config())
