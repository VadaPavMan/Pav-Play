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
        self.MainWindow = MainWindow
        self.setupWindow()
        # Main Layout
        self.setupMainLayout()

        # Navigation Bar 
        self.setupNavigationBar()

        # Media Layout
        self.setupMediaLayout()

        # Control Bar 
        self.setupControlsBar()
        
    def setupWindow(self):
        if not self.MainWindow.objectName():
            self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(WIDTH, HEIGHT)
            
    def setupMainLayout(self):
        self.centralWidget = QWidget()
        self.centralWidget.setStyleSheet("background-color: #121212")
        self.MainWindow.setCentralWidget(self.centralWidget)
        self.mainLayout = QVBoxLayout(self.centralWidget)
        # Spacing & Margins
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(10)
    
    def setupNavigationBar(self):
        # Navigation Bar #1E1E1E
        self.navFrame = QFrame()
        self.navFrame.setStyleSheet("""background-color: #C9C9C9;
                                    border-radius: 12px;""")
        self.navLayout = QHBoxLayout(self.navFrame)
        self.mainLayout.addWidget(self.navFrame, 1)
        
    def setupMediaLayout(self):
         # Media Layout #181818
        self.mediaFrame = QFrame()
        self.mediaFrame.setStyleSheet("""background-color: #8F8F8F;
                                      border-radius: 12px;""")
        
        self.mediaLayout = QHBoxLayout(self.mediaFrame)
        # Media Player Frame #282828
        self.playerFrame = QFrame()
        self.playerFrame.setStyleSheet("""background-color: #E6E6E6;
                                       border-radius: 12px;""")
        
        # Media Playlist Frame #282828
        self.playlistFrame = QFrame()
        self.playlistFrame.setStyleSheet("""background-color: #E6E6E6;
                                         border-radius: 12px;""")
        
        self.mediaLayout.addWidget(self.playerFrame, 4)
        self.mediaLayout.addWidget(self.playlistFrame, 1)
        self.mainLayout.addWidget(self.mediaFrame, 8)
    
    def setupControlsBar(self):
        # Control Bar #1E1E1E
        self.controlsFrame = QFrame()
        self.controlsFrame.setStyleSheet("""background-color: #C9C9C9;
                                         border-radius: 12px;
                                         """)
        self.mainLayout.addWidget(self.controlsFrame, 2)
        
    def addLabel(self, Text):
        label = QLabel(Text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label
