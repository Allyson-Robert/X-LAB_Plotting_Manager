from PyQt5 import QtWidgets


def dialog_print(window: QtWidgets.QMainWindow, title, contents):
    """
    Display text content inside a modal dialog with optional saving.

    The dialog contains:
    - A read-only text editor showing `contents`.
    - “OK” to close the dialog.
    - “SAVE” to delegate saving via `window.save_to_file`.

    Parameters
    ----------
    window : QMainWindow
        Parent window providing the save callback.
    title : str
        Dialog title bar text.
    contents : str
        Text content to display.
    """
    # Prepare a text edit widget to host the contents
    history_text_edit = QtWidgets.QTextEdit(window)
    history_text_edit.setPlainText(contents)

    # Initialise the window
    dialog = QtWidgets.QDialog(window)
    dialog.setWindowTitle(title)

    # Set a default width and minimum height for the dialog
    dialog.resize(600, 400)

    # Create a QVBoxLayout for the dialog
    layout = QtWidgets.QVBoxLayout(dialog)

    # Add the QTextEdit widget to the layout
    layout.addWidget(history_text_edit)

    # Create a QHBoxLayout and host buttons
    button_layout = QtWidgets.QHBoxLayout()
    ok_button = QtWidgets.QPushButton("OK")
    save_button = QtWidgets.QPushButton("SAVE")
    button_layout.addWidget(ok_button)
    button_layout.addWidget(save_button)

    # Add the button layout to the main layout
    layout.addLayout(button_layout)

    # Connect the "OK" button to close the dialog
    ok_button.clicked.connect(dialog.accept)
    save_button.clicked.connect(lambda: window.save_to_file(contents))

    # Show the dialog
    dialog.exec_()