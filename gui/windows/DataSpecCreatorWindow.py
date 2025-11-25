from PyQt5 import QtWidgets, uic
import dataspec_manager
import datetime, json, sys

from gui.utils.search_for_active_radio_button import search_for_first_active_radio_button
from gui.utils.split_camelCase import split_camel_case

# FEATURE REQUEST: Allow multiple device types to be compatible with the same set


class UiDataCreatorWindow(QtWidgets.QDialog):
    """
       Dialog for interactively creating new `DataSpec` instances.

       Overview
       --------
       This window guides the user through constructing a dataspec by:
       - Selecting a device type from a combobox.
       - Adding individual files with custom labels, or
       - Auto-generating filepaths from a directory according to a chosen structure.
       - Setting the experiment name and experiment date/time.

       Behaviour
       ---------
       - Maintains an internal `DataSpec` object that is updated as the user adds
         files or generates sets from directories.
       - Displays the current file mapping as formatted JSON in a plain-text widget.
       - Validates that both a name and at least one file are present before
         enabling the “Done” button.
       - On completion (`finish`), writes name, device type, and experiment
         datetime into the dataspec and closes with an accepted result.

       Parameters
       ----------
       devices : list[str], optional
           List of available device names to present in the device selection combo
           box. Defaults to a single `"N/A"` entry when not specified.
       """
    def __init__(self, devices: list[str] = ["N/A"]):
        super(UiDataCreatorWindow, self).__init__()

        # Load the UI,
        # Note that loadUI adds objects to 'self' using objectName
        uic.loadUi("gui/windows/DataSpecCreatorWindow.ui", self)

        self.dataspec = dataspec_manager.DataSpec(datetime.datetime.now().strftime("%Y.%m.%d_%H.%M.%S"))

        # Add the correct devices to the experiment combo box
        self.dataTypeCombo.addItems(devices)

        # Set date to today by default
        self.dateTimeEdit.setDateTime(datetime.datetime.now())

        # Set starting tab to manual dataspec creation
        self.tabWidget.setCurrentIndex(0)

        # Define widget action
        self.browseFilesBtn.clicked.connect(self.browse_files)
        self.browseDirBtn.clicked.connect(self.browse_dir)
        self.addLabelBtn.clicked.connect(self.add_file_to_set)
        self.generateBtn.clicked.connect(self.generate_set)
        self.resetBtn.clicked.connect(self.reset)
        self.doneBtn.clicked.connect(self.finish)

        # Enable button when all is filled
        self.showSetPlainText.textChanged.connect(self.button_state)
        self.nameEdit.textChanged.connect(self.button_state)

        # Show the app
        self.show()

    def get_dataspec(self) -> dataspec_manager.dataspec.DataSpec:
        return self.dataspec

    def browse_files(self):
        """
        # Open file selection dialog to get a file path and update gui when confirmed
        """
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "Open File")
        self.browseFilesText.setPlainText(file_name[0])

    def browse_dir(self):
        """
        # Open directory selection dialog to get a path and update gui when confirmed
        """
        dir_name = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.browseDirText.setPlainText(dir_name)

    def add_file_to_set(self):
        """
        # Gets the path and label and adds it to the current DataSpec instance while updating GUI
        """
        # Read name and legend label from gui
        file_name = self.browseFilesText.toPlainText()
        file_label = self.labelEdit.text()

        # Check for duplicate label
        if file_label in self.dataspec.get_labels():
            self.show_message(
                title="Duplicate Label",
                message="""This label has already been used. Choose another label and try again."""
            )
        else:
            # Add the file to the dataset and update the gui
            self.dataspec.set_structure_type("flat")
            self.dataspec.add_filepath(file_name, file_label)
            self.showSetPlainText.setPlainText(
                json.dumps(
                    self.dataspec.get_filepaths(),
                    indent=4,
                    separators=(',', ': ')
                )
            )
            self.browseFilesText.clear()

        # Empty label widget
        self.labelEdit.clear()

    def generate_set(self):
        """
        Automatically generate a set of filepaths based on a directory path. Will create nested structure if desired
        """
        path = self.browseDirText.toPlainText()

        # If path is not selected, show message and return None
        if not path:
            self.show_message(title="No directory selected", message="""No directory was selected, please select directory and try again""")
            return None

        # Construct the filepaths for this dataspec
        active_button = split_camel_case(search_for_first_active_radio_button(self).objectName())[0]
        errors = self.dataspec.construct_filepaths(root_dir=path, type=active_button)

        # Show the directories/files that were ignored to the user
        if errors != "":
            self.show_message(title="Files were ignored", message=errors)

        # Show the files in the gui
        self.showSetPlainText.setPlainText(
            json.dumps(
                self.dataspec.get_filepaths(),
                indent=4,
                separators=(',', ': ')
            )
        )
        self.dataspec.set_structure_type(active_button)

    def button_state(self):
        """ Only enable closing when some data was included """
        # TODO: hmmmmmmmmmmmm, should I be able to close the window if I mistakenly opened it?
        nameTxt = self.nameEdit.text()
        files = self.showSetPlainText.toPlainText()
        if (files != "") and (nameTxt != ""):
            self.doneBtn.setEnabled(True)
        else:
            self.doneBtn.setEnabled(False)

    @staticmethod
    def show_message(title, message):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        x = msg.exec_()

    def reset(self):
        """ Completely reset this UI by clearing all elements """
        self.nameEdit.clear()
        self.labelEdit.clear()
        self.browseDirText.clear()
        self.browseFilesText.clear()
        self.showSetPlainText.clear()
        self.button_state()

    def finish(self):
        """ Add name, device type,  and date and time dataspec before exiting """
        self.dataspec.set_name(self.nameEdit.text())
        self.dataspec.set_device(self.dataTypeCombo.currentText())
        experiment_date_time = self.dateTimeEdit.dateTime().toPyDateTime().strftime("%Y.%m.%d_%H.%M.%S")
        self.dataspec.set_experiment_date(experiment_date_time)

        self.done(1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UiDataCreatorWindow()
    app.exec_()
