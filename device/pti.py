from data.data_processors.scatter_data.fluorescence_data_processor import FluorescenceScatterDataProcessor
from data.datatypes.scatter_data.fluorescence_scatter import FluorescenceData
from device.device_worker import DeviceWorkerCore
from plotter.scatter_data_plotter import ScatterDataPlotter


class PTI(DeviceWorkerCore):
    def __init__(self, device, fileset, plot_type, legend, options):
        # super() delegates method calls to a parent
        super().__init__(device, fileset, plot_type, legend)

        self.options = options
        self.set_data_type(FluorescenceData)
        self.set_processor_type(FluorescenceScatterDataProcessor)

    def set_options(self, *args, **kwargs):
        pass

    def plot(self, title, legend):
        """
        Show the fluorescence spectrum
        """
        plotter = ScatterDataPlotter(title, "wavelength", "fluorescence")
        plotter.ready_plot(self.data_processors, legend)
        plotter.draw_plot()
