from PyQt5 import QtWidgets, QtCore
from gui.utils.get_qwidget_value import get_qwidget_value
from implementations.utils import constants
import datetime
import dataset_manager
from contracts.plotter_options import PlotterOptions
import implementations
import implementations.devices
from utils.logging import with_logging

@with_logging
def plot_manager(window, *args, **kwargs):
    """
        Orchestrate a plotting run in a background thread to keep the GUI responsive.

        Workflow
        --------
        1. Collect the selected file labels from the main window.
        2. Build a reduced `DataSet` containing only the selected files, colours,
           device, structure type, and name.
        3. Collect plotting options from the active device widget (via `alias`
           properties) and from global GUI controls, storing them in `PlotterOptions`.
        4. Resolve and instantiate the appropriate device worker class from the
           `implementations.devices.workers` namespace.
        5. Configure the worker with the reduced dataset, selected plot function,
           and options.
        6. Move the worker to a `QThread`, wire up progress/finished signals, and
           start the thread.

        The function logs a concise summary of the run (including a short run
        identifier) to the GUI console once the worker is started.

        Parameters
        ----------
        window : QMainWindow
            Main application window providing access to the dataset, widgets
            (file selection, stacked options, checkboxes, etc.), and console API.
        """

    # Grab the selected files for plotting and build a reduced dataset
    dataset_time = datetime.datetime.now().strftime(constants.DATETIME_FORMAT)
    experiment_time = window.dataset.get_experiment_date().strftime(constants.DATETIME_FORMAT)
    dataset_selection = dataset_manager.DataSet(dataset_time)
    dataset_selection.set_experiment_date(experiment_time)

    for item in window.selectedFilesList.selectedItems():
        lbl = item.text()

        structure = window.dataset.get_structure_type()
        dataset_selection.set_structure_type(structure)

        path = window.dataset.get_filepath(lbl)
        dataset_selection.add_filepath(path, lbl)

        colour = window.dataset.get_single_colour(lbl)
        dataset_selection.add_colour(colour, lbl)

    dataset_selection.set_device(window.dataset.get_device())
    dataset_selection.set_structure_type(window.dataset.get_structure_type())
    dataset_selection.set_name(window.dataset.get_name())

    # Recursively search for QWidget children with an alias to collect options and get their values
    # TODO: Options should be a class whose instance can be passed
    options = PlotterOptions()
    for option in window.stackedWidget.currentWidget().findChildren(QtWidgets.QWidget):
        alias = option.property("alias")
        if alias is not None:
            option_value = get_qwidget_value(option)
            if option_value is not None:
                options.add_option(label=alias, value=option_value)
    options.add_option(label="presentation", value=get_qwidget_value(window.presentationCheckBox))
    options.add_option(label="legend_title", value=get_qwidget_value(window.legendTitleLineEdit))

    # Instantiate proper device class and set the data
    current_device_class = window.dataset.get_device()
    device_module = getattr(implementations.devices.workers, current_device_class.lower())
    experiment_cls = getattr(device_module, current_device_class)

    # # Grab the correct plotting function and pass all options to it
    plot_function = window.get_current_plot_function()

    # Create a new thread for the device class to run in
    window.thread = QtCore.QThread()
    window.experiment_worker = experiment_cls(current_device_class, dataset_selection, plot_function, options=options)
    window.experiment_worker.moveToThread(window.thread)

    # Connect signals and slots for the worker thread
    window.thread.started.connect(window.experiment_worker.run)
    window.experiment_worker.finished.connect(window.thread.quit)
    window.experiment_worker.finished.connect(window.experiment_worker.deleteLater)
    window.thread.finished.connect(window.thread.deleteLater)
    window.experiment_worker.progress.connect(window.report_progress)

    # Start the thread
    window.thread.start()
    window.console_print(
        f"(run {window.experiment_worker.identifier}) producing {current_device_class}-{plot_function} plot for {window.get_dataset_name()} with options {options}")

    # FIXME: Final resets
    # window.longRunningBtn.setEnabled(False)
    # window.thread.finished.connect(
    #     lambda: window.longRunningBtn.setEnabled(True)
    # )
    # window.thread.finished.connect(
    #     lambda: window.stepLabel.setText("Long-Running Step: 0")
    # )