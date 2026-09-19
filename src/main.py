import os
import sys
os.environ.setdefault("QT_MULTIMEDIA_BACKEND", "ffmpeg")

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.icons import Icons
from src import ui


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = ui.MainUi()
        self.ui.setup(self)
        self.setWindowTitle("Pav Play")

    def closeEvent(self, event):
        self.ui.handleCloseEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(Icons.APPICON))
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
