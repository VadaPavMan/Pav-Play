import sys
import os
import random
from PySide6.QtCore import (
    QSize,
    Qt,
    QUrl,
    QTime,
    QPropertyAnimation,
    QEasingCurve,
    Property,
    QCoreApplication,
    QMetaObject,
    QRect,
)
from PySide6.QtGui import (
    QAction,
    QIcon,
    QPixmap,
    QFont,
    QKeyEvent,
    QDragEnterEvent,
    QDropEvent,
    QColor,
    QPalette,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QSplitter,
    QPushButton,
    QSlider,
    QLabel,
    QFileDialog,
    QMessageBox,
    QStatusBar,
    QToolBar,
    QStackedWidget,
    QSizePolicy,
    QMenu,
    QMenuBar,
    QFrame,
    QToolTip,
    QSpacerItem,
    QToolButton,
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget

WIDTH = 1280
HEIGHT = 720


class MainUi(object):
    def setup(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(WIDTH, HEIGHT)

        self.centralWidget = QWidget()
        MainWindow.setCentralWidget(self.centralWidget)

        # Main Layout
        self.mainLayout = QVBoxLayout(self.centralWidget)

        # Navigation Bar
        self.navFrame = QFrame()
        self.navFrame.setStyleSheet("""background-color: #f58442;
                                       border-radius: 12px;
                                       """)
        self.mainLayout.addWidget(self.navFrame, 1)

        # Media Layout
        self.mediaFrame = QFrame()
        self.mediaFrame.setStyleSheet("""
                                      background-color: #3b3b3b;
                                      border-radius: 12px;
                                      """)
        self.mainLayout.addWidget(self.mediaFrame, 8)

        # Control Bar
        self.controlsFrame = QFrame()
        self.controlsFrame.setStyleSheet("""background-color: #f58442;
                                       border-radius: 12px;
                                       """)
        self.mainLayout.addWidget(self.controlsFrame, 2)

    def addLabel(self, Text):
        label = QLabel(Text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label
