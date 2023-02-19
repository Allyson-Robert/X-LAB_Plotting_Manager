from data.data_processors.scatter_data.absorbance_data_processor import AbsorbanceScatterDataProcessor
from data.datatypes.scatter_data.absorbance_scatter import AbsorbanceScatterData
from plotter.scatter_data_plotter import ScatterDataPlotter
from experiment.experiment import Experiment
from fileset.fileset import Fileset


class DW2000(Experiment):
    def __init__(self):
        self.absorbance_processor = None

    def set_data(self,  fileset: Fileset):
        assert fileset.get_structure_type() == "flat"

        filepaths = fileset.get_filepaths()
        self.absorbance_processor = {}
        for key in filepaths:
            data = AbsorbanceScatterData(key)
            data.read_file(filepaths[key])
            self.absorbance_processor[key] = AbsorbanceScatterDataProcessor(data)

    def normal_plot(self, title, legend):
        plotter = ScatterDataPlotter(title, "wavelength", "absorbance")
        plotter.ready_plot(self.absorbance_processor, legend)
        plotter.draw_plot()

    def rainbow_plot(self, title, legend):
        # TODO: Add a rainbow plotting thing for a single file
        pass
