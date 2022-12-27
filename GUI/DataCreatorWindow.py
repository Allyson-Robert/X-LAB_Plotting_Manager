# Main.py
from PyQt5 import QtWidgets
from PyQt5 import uic
import sys
import json


class UiDataCreatorWindow(QtWidgets.QDialog):
    def __init__(self):
        super(UiDataCreatorWindow, self).__init__()

        # Load the UI,
        # Note that loadUI adds objects to 'self' using objectName
        uic.loadUi("DataCreatorWindow.ui", self)

        # Set properties
        self.data = {
            'name': '',
            'date': '',
            'device': '',
            'notes': '',
            'console': {},
            'files': []
        }

        # Define widget action
        self.browseBtn.clicked.connect(self.browse_files)
        self.doneBtn.clicked.connect(self.finish)
        self.addLabelBtn.clicked.connect(self.add_file_to_set)

        # Enable button when all is filled
        self.showSetPlainText.textChanged.connect(self.button_state)
        self.nameText.textChanged.connect(self.button_state)

        # Show the app
        self.show()

    def browse_files(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "Open File")
        self.browseText.setPlainText(file_name[0])

    def add_file_to_set(self):
        file_name = self.browseText.toPlainText()
        file_label = self.labelText.toPlainText()

        self.data['files'].append([file_name, file_label])
        self.showSetPlainText.setPlainText(
            json.dumps(
                self.data['files'],
                indent=4,
                separators=(',', ': ')
            )
        )
        self.browseText.clear()
        self.labelText.clear()

    def button_state(self):
        nameTxt = self.nameText.toPlainText()
        files = self.showSetPlainText.toPlainText()
        if (files != "") and (nameTxt != ""):
            self.doneBtn.setEnabled(True)
        else:
            self.doneBtn.setEnabled(False)

    def finish(self):
        self.data['name'] = self.nameText.toPlainText()
        self.data['date'] = '2022_12_24'
        self.data['device'] = self.dataTypeCombo.currentText()
        self.done(1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UiDataCreatorWindow()
    app.exec_()
