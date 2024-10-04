from PyQt5 import QtWidgets, QtCore
from utils.get_qwidget_value import get_qwidget_value
from utils import constants
import datetime
import fileset as fs
import json
import os

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


def plot_manager(window, config):
    """
        This can last a long time and will therefore instantiate a QThread to leave the gui responsive.
    """

    # Grab the selected files for plotting
    fileset_time = datetime.datetime.now().strftime(constants.DATETIME_FORMAT)
    experiment_time = window.fileset.get_experiment_date().strftime(constants.DATETIME_FORMAT)
    selected_fileset = fs.Fileset(fileset_time)
    selected_fileset.set_experiment_date(experiment_time)

    for item in window.selectedFilesList.selectedItems():
        lbl = item.text()
        path = window.fileset.get_filepath(lbl)
        selected_fileset.add_filepath(path, lbl)
        colour = window.fileset.get_colour(lbl)
        selected_fileset.add_colour(colour, lbl)

    selected_fileset.set_device(window.fileset.get_device())
    selected_fileset.set_structure_type(window.fileset.get_structure_type())
    selected_fileset.set_name(window.fileset.get_name())

    # Recursively search for QWidget children with an alias to collect options and get their values
    options_dict = {}
    for option in window.stackedWidget.currentWidget().findChildren(QtWidgets.QWidget):
        alias = option.property("alias")
        if alias is not None:
            options_dict[alias] = get_qwidget_value(option)
    options_dict["presentation"] = get_qwidget_value(window.presentationCheckBox)
    options_dict["legend_title"] = get_qwidget_value(window.legendTitleLineEdit)

    # Instantiate proper device class and set the data
    current_device_class = window.fileset.get_device()
    device_module = getattr(analysis.devices.workers, current_device_class.lower())
    experiment_cls = getattr(device_module, current_device_class)

    # # Grab the correct plotting function and pass all options to it
    plot_type = window.plotTypeCombo.currentText()
    window.console_print(
        f"Producing {current_device_class}-{plot_type} plot for {window.fileset.get_name()} with options {options_dict}")

    # Create a new thread for the device class to run in
    window.thread = QtCore.QThread()
    window.experiment_worker = experiment_cls(current_device_class, selected_fileset, plot_type, options=options_dict)
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