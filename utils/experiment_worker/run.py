from fileset.fileset import Fileset
from experiment.experiment_worker import ExperimentWorker


def run(fileset: Fileset, cls: ExperimentWorker, plot_type: str, legend: str):
    # Set the data
    cls.set_data(fileset)

    # Grab the correct plot and execute it
    plot_type = getattr(cls, plot_type)
    plot_type(title=fileset.get_name(), legend=legend)
