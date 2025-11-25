from abc import ABC, abstractmethod
from dataspec_manager.dataspec import DataSpec
from PyQt5 import QtCore
import uuid
from utils.logging import DEBUG_WORKER, decorate_class_with_logging
from contracts.plotter_options import PlotterOptions


# This custom metaclass is needed to make ABC and QObject multiple inheritance possible
#   Note: QObject provides default thread management tools
class WorkerMeta(type(ABC), type(QtCore.QObject)):
    """
        Metaclass enabling multiple inheritance of ABC and QObject.

        Overview:
            Resolves metaclass conflicts so `DeviceWorker` can be both an ABC
            and a Qt QObject.

        - Combines behavior of `ABC` and `QtCore.QObject` metatypes.

        Usage Notes:
            Use this metaclass only for worker classes that inherit from QObject.
    """
    pass


# Abstract baseclass to define worker objects and the required functions
class DeviceWorker(ABC, QtCore.QObject, metaclass=WorkerMeta):
    """
        Abstract base for device worker objects that run in a Qt context.

        Overview:
            Defines the required API for workers that accept a DataSpec,
            run a task, and accept data/processor types.

        - Required methods: set_data, run, set_data_type, set_processor_type.
        - Provides a short `identifier` used for run labelling.

        Usage Notes:
            Concrete workers should implement thread-safe run logic and emit signals.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.identifier = str(uuid.uuid4())[:4]

    @abstractmethod
    def set_data(self, dataspec: DataSpec):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def set_data_type(self, data_type):
        pass

    @abstractmethod
    def set_processor_type(self, processor_type):
        pass

@decorate_class_with_logging(log_level=DEBUG_WORKER)
class DeviceWorkerCore(DeviceWorker):
    """
        Concrete worker base implementing common setup and progress handling.

        Overview:
            Implements option handling, dataset instantiation and a simple run
            flow that prepares data processors, emits progress, and calls a plot.

        - Manages `device`, `dataspec`, `plot_type`, `options`, and `data_processors`.
        - Populates processors per-file and emits `progress`/`finished` signals.
        - `set_data_type` / `set_processor_type` are simple setters.

        Usage Notes:
            Subclasses provide plotting methods referenced by `plot_type` and may
            extend run behaviour if needed.
    """
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(int)

    def __init__(self, device, dataspec, plot_type, options: PlotterOptions):
        super().__init__()

        self.device = device
        self.dataspec = dataspec
        self.plot_type = plot_type

        self.options = options
        self.options.add_option(label="experiment_datetime", value = dataspec.get_experiment_date())


        self.data_processors = None

        self.processor_type = None
        self.data_type = None

    def set_data_type(self, data_type):
        self.data_type = data_type

    def set_processor_type(self, processor_type):
        self.processor_type = processor_type

    def set_data(self, dataspec: DataSpec):
        # CHECK: Check that dataspec and processor types have been set
        # Initialise an empty dict and get the required filepaths
        self.data_processors = {}
        filepaths = dataspec.get_filepaths()

        colours = dataspec.get_all_colours()
        if colours is not None:
            self.options.add_option(label="colours", value=colours)

        # Progress housekeeping
        nr_of_files = len(filepaths)
        counter = 0

        # Read the dataspec and instantiate a processor for each file
        for key in filepaths:
            data = self.data_type(key)
            data.read_file(filepaths[key])
            self.data_processors[key] = self.processor_type(data)

            # Emit progress signal
            counter += 1
            self.progress.emit(int(100*counter/nr_of_files))

    def run(self):
        # Set the data
        self.set_data(self.dataspec)

        # Grab the correct plot and execute it, including uuid in the title
        title = f"{self.dataspec.get_name()} (run {self.identifier})"
        plot_type = getattr(self, self.plot_type)
        plot_type(title=title)
        self.finished.emit()
