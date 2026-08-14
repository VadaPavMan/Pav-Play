from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from icons import Icons
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import ui


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = ui.MainUi()
        self.ui.setup(self)
        self.setWindowTitle("Pav Play")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(Icons.APPICON))
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
