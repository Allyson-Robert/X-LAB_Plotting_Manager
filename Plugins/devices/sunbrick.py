from plugins.data.data_processors.scatter_data.iv_data_processor import IVScatterDataProcessor
from plugins.data.data_types.scatter_data.iv_scatter import IVData
from plugins.devices.device_worker import DeviceWorkerCore
from plugins.plotter.scatter_data_plotter import ScatterDataPlotter


class Sunbrick(DeviceWorkerCore):
    """
         Implements the plotting function for the Sunbrick devices.
         Relevant data types and processors are IVData and IVScatterDataProcessor.
    """
    def __init__(self, device, fileset, plot_type, legend, options):
        super().__init__(device, fileset, plot_type, legend)

        self.presentation = None
        self.time_evolved = None
        self.options = options
        self.set_data_type(IVData)
        self.set_processor_type(IVScatterDataProcessor)

    def set_options(self, presentation: bool, time_evolved: bool, *args, **kwargs):
        self.presentation = presentation
        self.time_evolved = time_evolved

    def plot_fulliv(self, title, legend):
        plotter = ScatterDataPlotter(title, "voltage", "current")
        self._scatter_plot(plotter, legend)

    def plot_iv(self, title, legend):
        plotter = ScatterDataPlotter(title, "forward_voltage", "forward_current")
        self._scatter_plot(plotter, legend)

    def plot_fullpv(self, title, legend):
        plotter = ScatterDataPlotter(title, "voltage", "power")
        self._scatter_plot(plotter, legend)

    def plot_pv(self, title, legend):
        plotter = ScatterDataPlotter(title, "forward_voltage", "forward_power")
        self._scatter_plot(plotter, legend)

    def _scatter_plot(self, plotter: ScatterDataPlotter, legend: str):
        plotter.ready_plot(self.data_processors, legend)
        plotter.draw_plot(presentation=self.presentation, time_evolved=self.time_evolved)

    def print_parameters(self, *args, **kwargs):
        for lbl in self.data_processors:
            print(self.data_processors[lbl].get_data("parameters"))
