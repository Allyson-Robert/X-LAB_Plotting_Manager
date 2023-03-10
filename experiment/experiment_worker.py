from abc import ABC, ABCMeta, abstractmethod
from fileset.fileset import Fileset
from PyQt5 import QtCore


class WorkerMeta(type(ABC), type(QtCore.QObject)):
    pass


class ExperimentWorker(ABC, QtCore.QObject, metaclass=WorkerMeta):
    @abstractmethod
    def set_data(self,  fileset: Fileset):
        pass

    @abstractmethod
    def set_options(self,  *args, **kwargs):
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


class ExperimentWorkerCore(ExperimentWorker):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(int)

    def __init__(self, device, fileset, plot_type, legend):
        super().__init__()

        self.device = device
        self.fileset = fileset
        self.plot_type = plot_type
        self.legend = legend

        self.data_processors = None

        self.processor_type = None
        self.data_type = None

    @abstractmethod
    def set_options(self, *args, **kwargs):
        pass

    def set_data_type(self, data_type):
        self.data_type = data_type

    def set_processor_type(self, processor_type):
        self.processor_type = processor_type

    def set_data(self, fileset: Fileset):
        # TODO: Check that data and processor types have been set
        # Initialise an empty dict and get the required filepaths
        self.data_processors = {}
        filepaths = fileset.get_filepaths()

        # Progress housekeeping
        nr_of_files = len(filepaths)
        counter = 0

        # Read the data and instantiate a processor for each file
        for key in filepaths:
            data = self.data_type(key)
            data.read_file(filepaths[key])
            self.data_processors[key] = self.processor_type(data)

            # Emit progress signal
            self.progress.emit(int(100*counter/nr_of_files))
            counter += 1

    def run(self):
        # Set the data
        self.set_data(self.fileset)

        # Pass the options
        self.set_options(**self.options)

        # Grab the correct plot and execute it
        plot_type = getattr(self, self.plot_type)
        plot_type(title=self.fileset.get_name(), legend=self.legend)
        self.finished.emit()
