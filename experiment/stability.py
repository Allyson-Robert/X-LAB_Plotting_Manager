from data.data_processors.iv_stability_dataprocessor import IVStabilityDataProcessor
from data.datatypes.scatter_data.iv_scatter import IVScatterData
from plotter.iv_stability_plotter import IVStabilityPlotter
from fileset.fileset import Fileset
from fileset.fileset_json_encoder import FilesetJSONEncoder
import json


class Stability:
    def __init__(self):
        self.iv_stability_processors = None

    def set_data(self, fileset: Fileset):
        # assert fileset.get_structure_type() == "structured"

        filepaths = fileset.get_filepaths()
        self.iv_stability_processors = {}
        for key in filepaths:
            processors_list = []
            for label in filepaths[key]:
                iv_data = IVScatterData(label)
                iv_data.read_file(filepaths[key][label])
                processors_list.append(iv_data)
            self.iv_stability_processors[key] = IVStabilityDataProcessor(processors_list)

    def plot_four(self, title, legend):
        plotter = IVStabilityPlotter(title)
        plotter.ready_plot(self.iv_stability_processors, legend)
        plotter.draw_plot()
