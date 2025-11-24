from PyQt5 import QtWidgets, QtCore, QtGui


def generate_about_dialog(about_contents, centralwidget, logo_path):
    # Create a custom QDialog for the about information
    about_dialog = QtWidgets.QDialog(centralwidget)
    about_dialog.setWindowTitle("About")

    # Set the fixed size of the dialog
    about_dialog.setFixedSize(650, 700)  # Adjust the dimensions as needed

    # Load and set the image using QPixmap (make sure the path is correct)
    pixmap = QtGui.QPixmap(logo_path + "X_logo_x-lab_baseline_KL.png")
    pixmap = pixmap.scaled(600, 200, QtCore.Qt.KeepAspectRatio)
    image_label = QtWidgets.QLabel(about_dialog)
    image_label.setPixmap(pixmap)

    # Create a QLabel for the text (using HTML formatting)
    text_label = QtWidgets.QLabel(about_dialog)
    text_label.setWordWrap(True)
    text_label.setText(about_contents)

    # Create a QVBoxLayout for the dialog and add the image and text labels
    layout = QtWidgets.QVBoxLayout(about_dialog)
    layout.addWidget(image_label)
    layout.addWidget(text_label)

    about_dialog.setLayout(layout)

    return about_dialog