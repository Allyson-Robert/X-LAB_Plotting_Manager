from typing import Type
from fileset.fileset import Fileset
from experiment.experiment_worker import ExperimentWorker
from data.datatypes.scatter_data.scatter import ScatterData
from data.data_processors.scatter_data.data_processors import ScatterDataProcessor


def run(fileset: Fileset, cls: ExperimentWorker, plot_type: str, legend: str):
    # Set the data
    cls.set_data(fileset)

    # Grab the correct plot and execute it
    plot_type = getattr(cls, plot_type)
    plot_type(title=fileset.get_name(), legend=legend)
