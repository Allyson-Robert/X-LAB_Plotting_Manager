# Main.py
from PyQt5 import QtWidgets
from PyQt5 import uic
import sys
import json
import DataCreatorWindow
import data_readers_plotly as drp
import datetime


class UiMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(UiMainWindow, self).__init__()

        # Define properties
        self.init_data = {
            'name': '',
            'date': '',
            'device': '',
            'notes': '',
            'console': {},
            'files': []
        }
        self.data = self.init_data.copy()
        self.devices = {
            '': 0,
            'Sunbrick': 1,
            'DW2000': 2,
            'LBIC': 3,
            'PDS': 4,
            'PTI': 5
        }  # Keeps track of the widget index in stackedWidget for each type of device
        self.plot_types = {
            'Sunbrick': ['plot_iv', 'plot_fulliv', 'plot_pv', 'print'],
            'DW2000': ['plot', 'plot_rainbow'],
            'LBIC': ['show_image', 'plot_intensities', 'plot_horiz_profile'],
            'PDS': ['plot'],
            'PTI': ['plot'],
        }

        # Load the UI,
        # Note that loadUI adds objects to 'self' using objectName
        self.dataWindow = None
        uic.loadUi("MainWindow.ui", self)

        # Reset stacked widget to empty page
        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(0))

        # Define widget action
        self.actionQuit.triggered.connect(self.quit)

        self.actionCreate.triggered.connect(self.create_data)
        self.actionSave.triggered.connect(self.save_data)
        self.actionLoad.triggered.connect(self.open_data_file)

        self.actionAbout.triggered.connect(self.show_about)

        self.showDataBtn.clicked.connect(self.display_data)
        self.showHistoryBtn.clicked.connect(self.display_history)
        self.addNotesBtn.clicked.connect(self.add_notes)

        self.appendBtn.clicked.connect(self.append_console_to_set)
        self.clearBtn.clicked.connect(self.clear_data)
        self.clearAllBtn.clicked.connect(self.clear_all)
        self.quitBtn.clicked.connect(self.quit)

        # Define stackedWidget widget actions
        self.lbicProfilesCheckBox.stateChanged.connect(self.toggle_lbic_profile)
        self.plotBtn.clicked.connect(self.plot)

        # Show the app
        self.show()

    def create_data(self):
        self.dataWindow = DataCreatorWindow.UiDataCreatorWindow()
        self.dataWindow.show()
        if self.dataWindow.exec() == 1:
            self.data = self.dataWindow.data.copy()
            self.console_print(f"Dataset created")
            self.console_print("Warning: Dataset must be saved")
            self.load_data(self.data['device'])
            self.update_header()
        else:
            self.console_print("No data was created")

    def save_data(self):
        if not self.data:
            self.console_print("Err: Must first load data")
            return 1
        file_name = QtWidgets.QFileDialog.getSaveFileName(self, "Save file to disk")[0]
        if file_name != "":
            with open(file_name, "w") as json_file:
                json.dump(self.data, json_file)
            json_file.close()
            self.console_print(f"Saved data to {file_name}")
        else:
            self.console_print(f"No file selected")

    def open_data_file(self):
        self.clear_data()
        self.consolePlainText.clear()
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "Open Files")[0]
        if file_name != '':
            with open(file_name) as json_file:
                self.data = json.load(json_file)
                self.console_print(f"Opened {file_name}")
            self.notesPlainText.setPlainText(self.data['notes'])
            self.load_data(self.data['device'])
            self.update_header()
        else:
            self.console_print(f"Err: No file loaded")

    def load_data(self, plot_type):
        for file in self.data['files']:
            self.selectedFilesList.addItem(file[1])
        # For lbic plot type set selection to first item, otherwise select all
        if self.data['device'] == "LBIC":
            self.selectedFilesList.setCurrentRow(0)
        else:
            self.selectedFilesList.selectAll()

        for plot_type in self.plot_types[self.data['device']]:
            self.plotTypeCombo.addItem(plot_type)
        self.console_print("Data loaded")

    def display_data(self):
        # Width should probably be changed
        if not self.data:
            self.console_print("Err: Must first load data")
            return 1
        pretty_json = json.dumps(
            self.data,
            indent=4,
            separators=(',', ': ')
        )
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(f"Dataset: {self.data['name']}")
        msg.setText(pretty_json)
        x = msg.exec_()

    def display_history(self):
        # Will require a scroll area for long histories
        if not self.data:
            self.console_print("Err: Must first load data")
            return 1

        pretty_history = ""
        for k, v in sorted(self.data['console'].items()):
            line = f"{v}\n"
            pretty_history += line
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(f"Dataset: {self.data['name']}")
        msg.setText(pretty_history)
        x = msg.exec_()

    def add_notes(self):
        self.data['notes'] = self.notesPlainText.toPlainText()
        self.console_print("Notes added to dataset")
        self.console_print("Warning: Changes must be saved")

    def update_header(self):
        self.currSetNameLineEdit.setText(self.data['name'])
        self.currDeviceLineEdit.setText(self.data['device'])
        self.update_stacked_widget()

    def update_stacked_widget(self):
        new_page = self.stackedWidget.widget(self.devices[self.data['device']])
        self.stackedWidget.setCurrentWidget(new_page)

    def plot(self):
        self.console_print(f"Producing plot for {self.data['name']}")
        selected_files = []
        for item in self.selectedFilesList.selectedItems():
            for line in self.data['files']:
                # Check whether the label fits the label from the listWidget
                if item.text() == line[1]:
                    selected_files.append(line)

        device = self.data['device']
        plot_type = self.plotTypeCombo.currentText()

        if device == "Sunbrick":
            return_str = self.plot_sunbrick(plot_type, selected_files)
        elif device == "DW2000":
            return_str = self.plot_dw2000(plot_type, selected_files)
        elif device == "LBIC":
            return_str = self.plot_lbic(plot_type, selected_files)
        elif device == "PDS":
            return_str = self.plot_pds(plot_type, selected_files)
        elif device == "PTI":
            return_str = self.plot_pti(plot_type, selected_files)
        else:
            return_str = "Err: Unknown device type"

        self.console_print(return_str)

    def plot_sunbrick(self, plot_type, selected_files):
        reader = drp.Sunbrick(selected_files)
        p = self.presentationCheckBox.isChecked()
        if plot_type == "plot_iv":
            return reader.plot_iv(title=self.data['name'], presentation=p)
        elif plot_type == "plot_fulliv":
            return reader.plot_fulliv(title=self.data['name'])
        elif plot_type == "plot_pv":
            return reader.plot_pv(title=self.data['name'])
        else:
            return "Unknown plot type, skipped action."

    def plot_dw2000(self, plot_type, selected_files):
        reader = drp.DW2000(self.data['name'])
        if plot_type == "plot":
            return reader.plot(selected_files)
        elif plot_type == "plot_rainbow":
            return reader.plot_rainbow(selected_files)
        else:
            return "Unknown plot type, skipped action."

    def toggle_lbic_profile(self):
        if self.lbicProfilesCheckBox.isChecked():
            self.lbicProfilesSpinBox.setEnabled(True)
        else:
            self.lbicProfilesSpinBox.setDisabled(True)

    def plot_lbic(self, plot_type, selected_files):
        if len(selected_files) != 1:
            # Note to self: batch production should be possible now using the label as a title
            return "LBIC only produces one image at a time"

        reader = drp.LBIC(self.data['name'])
        profiles = self.lbicProfilesCheckBox.isChecked()
        if plot_type == "show_image":
            # Gather UI info before plotting
            intensities = [
                self.intRangeLowSpinBox.value() * 10**(-6),
                self.intRangeUpSpinBox.value() * 10**(-6)
            ]
            self.console_print(f"Range set to {intensities} A")
            return reader.show_image(selected_files, range=intensities, profiles=profiles)

        elif plot_type == "plot_intensities":
            return reader.plot_intensities(selected_files)

        elif plot_type == "plot_horiz_profile":
            if profiles:
                ycoord = self.lbicProfilesSpinBox.value()
                return reader.plot_horiz_profile(selected_files, ycoord)
            else:
                return "Must enable profile for this plot"
        else:
            return "Unknown plot type, skipped action."

    def plot_pds(self, plot_type, selected_files):
        reader = drp.PDS(self.data['name'])
        n = self.pdsNormCheckBox.isChecked()
        p = self.presentationCheckBox.isChecked()
        if plot_type == "plot":
            return reader.plot(selected_files, normalised=n, presentation=p)
        else:
            return "Unknown plot type, skipped action."

    def plot_pti(self, plot_type, selected_files):
        reader = drp.PtiText(self.data['name'])
        if plot_type == "plot":
            return reader.plot(selected_files)
        else:
            return "Unknown plot type, skipped action."

    def console_print(self, fstring):
        now = datetime.datetime.now()
        self.consolePlainText.appendPlainText(now.strftime("%d/%m/%Y %H.%M.%S: ") + fstring)

    def append_console_to_set(self):
        console_text = self.consolePlainText.toPlainText()
        now = datetime.datetime.now()
        self.data['console'][now.strftime("%d%m%Y_%H%M%S")] = console_text
        self.console_print("Added console contents to set")

    def clear_data(self):
        self.data = self.init_data.copy()

        self.currSetNameLineEdit.clear()
        self.currDeviceLineEdit.clear()
        self.notesPlainText.clear()
        self.console_print("Cleared data from memory")

        self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(0))
        self.selectedFilesList.clear()
        self.plotTypeCombo.clear()

    def clear_all(self):
        self.clear_data()
        self.consolePlainText.clear()
        self.console_print("Cleared memory")

    def show_about(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("About")
        msg.setText("""Plotting GUI \nVersion number: v1.0.1\nLast update: 2022/12/26""")
        x = msg.exec_()

    @staticmethod
    def quit():
        sys.exit()


app = QtWidgets.QApplication(sys.argv)
window = UiMainWindow()
app.exec_()
