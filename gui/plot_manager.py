from PyQt5 import QtWidgets, QtCore
from utils.get_qwidget_value import get_qwidget_value
from utils import constants
import datetime
import dataspec_manager
import json
import os
from analysis.plotters.plotter_options import PlotterOptions

# TODO: There has to be a better way
# Read the JSON config file
if os.name == "nt":
    config_file = 'config_win.json'
else:
    config_file = 'config_linux.json'

with open(config_file) as f:
    config = json.load(f)

# Get the analysis package path
analysis_path = config['analysis_path']

# Get the analysis package path
analysis_path = config['analysis_path']

# Add the analysis package path to the system path and import it
import sys
sys.path.insert(0, analysis_path)
sys.path.append("../..")
import analysis.devices


# This plot manager
#     collects the filenames
#     builds a custom dataspec for plotting by copying from main window
#     collects the options
#     instantiates Class by importing module and class
#     grab plot_function
#     creates, connects and starts a worker thread
def plot_manager(window, config):
    """
        This can last a long time and will therefore instantiate a QThread to leave the gui responsive.
    """

    # Grab the selected files for plotting and build a reduced dataspec
    dataspec_time = datetime.datetime.now().strftime(constants.DATETIME_FORMAT)
    experiment_time = window.dataspec.get_experiment_date().strftime(constants.DATETIME_FORMAT)
    dataspec_selection = dataspec_manager.DataSpec(dataspec_time)
    dataspec_selection.set_experiment_date(experiment_time)

    for item in window.selectedFilesList.selectedItems():
        lbl = item.text()
        path = window.dataspec.get_filepath(lbl)
        dataspec_selection.add_filepath(path, lbl)
        colour = window.dataspec.get_single_colour(lbl)
        dataspec_selection.add_colour(colour, lbl)

    dataspec_selection.set_device(window.dataspec.get_device())
    dataspec_selection.set_structure_type(window.dataspec.get_structure_type())
    dataspec_selection.set_name(window.dataspec.get_name())

    # Recursively search for QWidget children with an alias to collect options and get their values
    # TODO: Options should be a class whose instance can be passed
    options = PlotterOptions()
    for option in window.stackedWidget.currentWidget().findChildren(QtWidgets.QWidget):
        alias = option.property("alias")
        if alias is not None:
            options.add_option(label = alias, value = get_qwidget_value(option))
    options.add_option(label="presentation", value = get_qwidget_value(window.presentationCheckBox))
    options.add_option(label="legend_title", value = get_qwidget_value(window.legendTitleLineEdit))

    # Instantiate proper device class and set the data
    current_device_class = window.dataspec.get_device()
    device_module = getattr(analysis.devices.workers, current_device_class.lower())
    experiment_cls = getattr(device_module, current_device_class)

    # # Grab the correct plotting function and pass all options to it
    plot_function = window.get_current_plot_function()
    window.console_print(
        f"Producing {current_device_class}-{plot_function} plot for {window.get_dataspec_name()} with options {options}")

    # Create a new thread for the device class to run in
    window.thread = QtCore.QThread()
    window.experiment_worker = experiment_cls(current_device_class, dataspec_selection, plot_function, options=options)
    window.experiment_worker.moveToThread(window.thread)

    # Connect signals and slots for the worker thread
    window.thread.started.connect(window.experiment_worker.run)
    window.experiment_worker.finished.connect(window.thread.quit)
    window.experiment_worker.finished.connect(window.experiment_worker.deleteLater)
    window.thread.finished.connect(window.thread.deleteLater)
    window.experiment_worker.progress.connect(window.report_progress)

    # Start the thread
    window.thread.start()

    # FIXME: Final resets
    # window.longRunningBtn.setEnabled(False)
    # window.thread.finished.connect(
    #     lambda: window.longRunningBtn.setEnabled(True)
    # )
    # window.thread.finished.connect(
    #     lambda: window.stepLabel.setText("Long-Running Step: 0")
    # )