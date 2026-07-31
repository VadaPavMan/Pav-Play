from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
import ui
import sys
import os

WIDTH = 1280
HEIGHT = 720
       
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Music Player")
#         self.resize(QSize(WIDTH, HEIGHT))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = ui.MainUi()
        self.ui.setup(self)
        self.ui.addLabel("This is the label")
        self.setWindowTitle("Music Player")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets\\appIcon.png"))
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())