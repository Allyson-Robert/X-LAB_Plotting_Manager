# Extend the path to include the source root as well as gui root
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
CWD = Path.cwd().resolve()

for path in {PROJECT_ROOT, CWD}:
    s = str(path)
    if s not in sys.path:
        sys.path.insert(0, s)

# Generic dependency imports
import importlib, datetime, json, logging, sys
from PyQt5 import QtWidgets, uic, QtCore

# Functional programming imports
from functools import partial

# Local imports
import dataset_manager
import implementations.utils.constants
from utils.class_utils.get_class_methods import get_class_methods
from utils.console_colours import ConsoleColours
from utils.read_config import read_config

# Local gui imports
from gui.windows.dialogs.generate_about_dialog import generate_about_dialog
from gui.utils.clear.clear_data import clear_data
from gui.utils.clear.clear_all import clear_all

# DataSet file imports
from gui.utils.dataset_tools.load_dataset import open_dataset_file
from gui.utils.dataset_tools.save_dataset import save_dataset
from gui.utils.dataset_tools.create_dataset import create_dataset

# Dialog imports
from gui.windows.dialogs.dialog_print import dialog_print

# Plot manager imports
from gui.plot_manager import plot_manager

# Import relative paths from gui.utils.paths
import gui.utils.paths as CONSTANT_PATHS

# Check that the implementations package is available and complete
from utils.check_implementations import check_implementations, ImplementationError
try:
    check_implementations()
except (ImportError, FileNotFoundError, ImplementationError) as exc:
    print("Cannot start GUI, implementations package not found or incomplete.")
    raise exc

import implementations.devices as devices
from implementations.utils import constants

class UiMainWindow(QtWidgets.QMainWindow):
    """
    Main GUI window for interactive, automated plotting of experimental data.

    Responsibilities
    ----------------
    - Load the main QtDesigner-generated UI file and dynamically attach device-
      specific option panels to the central `QStackedWidget`.
    - Manage the currently loaded `DataSet`:
        * Creating, loading, saving, and autosaving datasets.
        * Displaying raw JSON content and console history in helper dialogs.
        * Updating header fields (set name, device type) when datasets change.
    - Integrate logging with a QTextEdit-based console for time-stamped messages.
    - Provide a thin controller layer for:
        * Launching the plotting pipeline via `plot_manager`.
        * Handling progress updates and console appends.
        * Adding notes and console history back into the dataset.

    On construction, the window:
    - Discovers available devices from `implementations.devices`.
    - Loads and registers per-device widgets and their plot functions.
    - Wires menu actions and buttons to dataset, plotting, and utility actions.
    - Optionally auto-opens a demo dataset if a file name is supplied.

    The class is intended to be the central hub of the GUI application, with
    device-specific logic pushed into worker classes and implementations.
    """
    def __init__(self, demo_file_name: str = None):
        super(UiMainWindow, self).__init__()

        self.thread = None
        self.experiment_worker = None
        self.dataset = None
        self.dataset_location = None

        # Load the UI, Note that loadUI adds objects to 'self' using objectName
        self.dataWindow = None
        uic.loadUi(CONSTANT_PATHS.WINDOW_PATH, self)

        # Read the config file
        self.config = read_config(CONSTANT_PATHS.CONFIG_PATH)

        # Create/Get a logger with the desired settings
        self.logger = logging.getLogger(constants.LOG_NAME)
        self.consoleTextEdit.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)8.8s] %(message)s",
                datefmt=f'{constants.DATETIME_FORMAT}: '
            )
        )
        self.logger.addHandler(self.consoleTextEdit)
        self.logger.setLevel(self.config['log_level'])

        self.plot_functions = {}
        self.devices = {}

        # Get list of devices as defined manually in the.devices __init__.py file
        for entry in devices.__all__:
            # Find and load the widget for any given device and add it to the stackedWidget
            entry_ui_file = entry.lower() + ".ui"
            entry_widget = uic.loadUi(CONSTANT_PATHS.WIDGET_PATH + entry_ui_file)
            entry_index = self.stackedWidget.addWidget(entry_widget)
            self.devices[entry] = entry_index

            # Import the corresponding module and get the class methods to set the plot_functions combobox when needed
            module = importlib.import_module(f"{devices.workers.__name__}.{entry.lower()}")
            entry_cls = getattr(module, entry)
            self.plot_functions[entry] = get_class_methods(entry_cls, ignore=["run"])

        # Reset stacked widget to empty page
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(0))

        # Define menubar actions
        self.actionCreate_Set.triggered.connect(partial(create_dataset, self))
        self.actionSave_Set.triggered.connect(partial(save_dataset, self))
        self.actionLoad_Set.triggered.connect(partial(open_dataset_file, self))
        self.actionPreferences.triggered.connect(self.not_implemented)
        self.actionQuit.triggered.connect(self.quit)

        self.actionSave_format.triggered.connect(self.not_implemented)
        self.actionColour_scheme.triggered.connect(self.not_implemented)
        self.actionLine_width.triggered.connect(self.not_implemented)

        self.actionDocumentation.triggered.connect(self.navigate_to_docs)
        self.actionAbout.triggered.connect(self.show_about)

        # Define gui button actions
        self.showDataBtn.clicked.connect(self.display_data)
        self.showHistoryBtn.clicked.connect(self.display_history)
        self.addNotesBtn.clicked.connect(self.add_notes)

        self.appendBtn.clicked.connect(self.append_console_to_set)
        self.clearBtn.clicked.connect(partial(clear_data, window=self))
        self.clearAllBtn.clicked.connect(partial(clear_all, window=self))
        self.quitBtn.clicked.connect(self.quit)

        # Define stackedWidget widget actions
        self.plotBtn.clicked.connect(partial(plot_manager, self))

        # Make sure the progress bar is cleared
        self.progressBar.setValue(0)

        # Show the app
        self.show()
        self.console_print("Program Started")

    # Getters
    def get_plot_functions(self, device='Generic') -> list:
        return self.plot_functions[device]

    def get_current_plot_function(self) -> str:
        return self.plotTypeCombo.currentText()

    def get_current_device(self) -> str:
        return self.dataset.get_device()

    def get_dataset(self):
        return self.dataset

    def get_dataset_name(self) -> str:
        if self.dataset is None:
            return None
        return self.dataset.get_name()

    def get_dataset_window(self) -> QtWidgets.QDialog:
        return self.dataWindow

    # Setters
    def set_dataset_window(self, dataset_window: QtWidgets.QDialog):
        self.dataWindow = dataset_window

    def set_dataset(self, dataset: dataset_manager.dataset.DataSet):
        self.dataset = dataset

    # FUNCTIONALITY
    def autosave(self):
        file_name = self.dataset.get_location()
        if file_name is None:
            return self.console_print("Cannot autosave, no file location known. Open or create dataset first")

        with open(file_name, "w") as json_file:
            json.dump(self.dataset, json_file, cls=dataset_manager.DataSetJSONDecoder)
        json_file.close()

        return self.console_print(f"Saved dataset to {file_name}")

    def display_data(self):
        # Abort if no dataset was loaded
        if self.dataset is None:
            return self.console_print("Err: Must first load DataSet", level="warning")

        # Pretty print the dataset in a simple dialog
        pretty_json = json.dumps(
            self.dataset,
            indent=4,
            separators=(',', ': '),
            cls=dataset_manager.DataSetJSONDecoder
        )
        dialog_print(window=self, title=f"DataSet RAW: {self.dataset.get_name()}", contents=pretty_json)

        return None

    def display_history(self):
        if self.dataset is None:
            return self.console_print("Err: Must first load DataSet", level="warning")

        # Prints only the console history to a simple dialog
        pretty_history = ""
        for k, v in sorted(self.dataset.get_console().items()):
            line = f"{v}\n"
            pretty_history += line

        dialog_print(window=self, title=f"DataSet History: {self.dataset.get_name()}", contents=pretty_history)

        return None

    def add_notes(self):
        if self.dataset is None:
            return self.console_print("Err: Must first load DataSet", level="warning")

        # Add any notes to the dataset_manager with a trailing new line
        self.dataset.add_notes(self.notesPlainText.toPlainText() + "\n")
        self.console_print("Notes added to dataset_manager")
        self.autosave()

        return None

    def update_header(self):
        # Header should reflect opened dataset
        self.currSetNameLineEdit.setText(self.dataset.get_name())
        self.currDeviceLineEdit.setText(self.dataset.get_device())

        # Stacked widget should show the correct widget for the opened dataset
        new_page = self.stackedWidget.widget(self.devices[self.dataset.get_device()])
        self.stackedWidget.setCurrentWidget(new_page)

    def report_progress(self, progress: int):
        if not (isinstance(progress, int) and 0 <= progress <= 100):
            raise ValueError("Progress must be an integer between 0 and 100")

        self.progressBar.setValue(progress)

    def save_to_file(self, plaintext: str):
        file_dialog = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_dialog[0]:  # Check if a file was selected
            file_path = file_dialog[0]
            with open(file_path, 'w') as file:
                file.write(plaintext)

    def console_print(self, fstring, level="normal"):
        # Print a message to the gui console
        now = datetime.datetime.now()
        fstring_to_print = now.strftime(f"{constants.DATETIME_FORMAT}: ") + fstring

        c = ConsoleColours()

        self.consoleTextEdit.setTextColor(c.get_colour(level))
        self.consoleTextEdit.append(fstring_to_print)
        self.consoleTextEdit.setTextColor(c.get_colour("normal"))

    def append_console_to_set(self):
        if self.dataset is None:
            return self.console_print("Err: Must first load DataSet", level="warning")

        # Append console contents to the dataset_manager
        console_text = self.consoleTextEdit.toPlainText()
        now = datetime.datetime.now()
        self.dataset.add_console(now.strftime(constants.DATETIME_FORMAT), console_text)
        self.console_print("Added console contents to set")
        self.autosave()

        return None

    def show_about(self):
        """
            Shows a simple window with licence, authorship and build information
        """
        # Grab the "about" info from about.txt
        with open(CONSTANT_PATHS.ABOUT_PATH) as about_file:
            about_contents = about_file.read()

        about_dialog = generate_about_dialog(about_contents, self.centralWidget(), gui.utils.paths.LOGO_PATH)

        # Show the about dialog
        about_dialog.exec_()

    def navigate_to_docs(self):
        """
            Opens the default web browser and navigates to the documentation URL.
        """
        import webbrowser
        webbrowser.open(CONSTANT_PATHS.DOCS_URL)

    def not_implemented(self):
        """
            Shows the user a message that the current feature is planned but not yet implemented.
        """
        self.console_print("Feature not implemented", level='warning')

    # ESC now triggers a program exit
    def keyPressEvent(self, event) -> None:
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.quit()
        else:
            super(UiMainWindow, self).keyPressEvent(event)

    # CHECK: Program exit is not safe
    @staticmethod
    def quit():
        # Terminate the application
        sys.exit()


if __name__ == "__main__":
    # Enable high-DPI scaling and per-monitor awareness
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    # Initialise app, window and start execution
    app = QtWidgets.QApplication(sys.argv)
    window = UiMainWindow()
    app.exec_()
