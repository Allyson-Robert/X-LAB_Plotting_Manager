from gui.windows.MainWindow import UiMainWindow
from PyQt5 import QtWidgets
import sys
import os

# Add the path to the gui/windows directory to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
windows_dir = os.path.join(parent_dir, 'gui', 'windows')
sys.path.append(windows_dir)

if __name__ == "__main__":
    # Initialise app, window and start execution
    app = QtWidgets.QApplication(sys.argv)
    filename = "G:\\My Drive\\Data\\Sunbrick\\Datasets\\2024_04_24_12_37_00_Sx_5-4-2-1_PM6-Y6_M2-test-stabilityset.json"
    window = UiMainWindow(filename)
    app.exec_()
