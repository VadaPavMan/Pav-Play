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
    def __init__(self): ...

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
        # Navigation Bar Dark: #1E1E1E White: #C9C9C9
        self.navFrame = QFrame()
        self.navFrame.setStyleSheet("""background-color: #1E1E1E;
                                    border-radius: 12px;""")
        self.navLayout = QHBoxLayout(self.navFrame)
        self.navLayout.setSpacing(20)

        # Nav bar buttons

        # AppIcon Button
        self.logoButton = QPushButton("")
        self.logoButton.setIcon(QIcon("assets\\appicon.png"))
        self.logoButton.setIconSize(QSize(32, 32))
        self.logoButton.setFlat(True)
        self.logoButton.setStyleSheet("border: none; background: transparent;")
        self.navLayout.addWidget(self.logoButton)

        # OpenFile Button
        self.openFileButton = QPushButton("Open File")
        self.openFileButton.setIcon(QIcon("assets\\files.png"))
        self.openFileButton.setIconSize(QSize(32, 32))
        self.openFileButton.setFlat(True)
        self.openFileButton.setStyleSheet(
            "border: none; background: transparent; color: white; font-weight: bold;"
        )
        self.navLayout.addWidget(self.openFileButton)

        # OpenFolder Button
        self.openFolderButton = QPushButton("Open Folder")
        self.openFolderButton.setIcon(QIcon("assets\\folder.png"))
        self.openFolderButton.setIconSize(QSize(32, 32))
        self.openFolderButton.setFlat(True)
        self.openFolderButton.setStyleSheet(
            "border: none; background: transparent; color: white; font-weight: bold;"
        )
        self.navLayout.addWidget(self.openFolderButton)

        # ThemeToggle Button
        self.themeToggleButton = QPushButton("Theme Toggle")
        self.themeToggleButton.setIcon(QIcon("assets\\theme.png"))
        self.themeToggleButton.setIconSize(QSize(38, 38))
        self.themeToggleButton.setFlat(True)
        self.themeToggleButton.setStyleSheet(
            "border: none; background: transparent; color: white; font-weight: bold;"
        )
        self.navLayout.addWidget(self.themeToggleButton)

        # Settings Button
        self.navLayout.addStretch()
        self.settingsButton = QPushButton("Settings")
        self.settingsButton.setIcon(QIcon("assets\\settings.png"))
        self.settingsButton.setIconSize(QSize(32, 32))
        self.settingsButton.setFlat(True)
        self.settingsButton.setStyleSheet(
            "border: none; background: transparent; color: white; font-weight: bold;"
        )
        self.navLayout.addWidget(self.settingsButton)

        self.mainLayout.addWidget(self.navFrame, 1)

    def setupMediaLayout(self):
        # Media Layout Dark: #181818 White: #8F8F8F
        self.mediaFrame = QFrame()
        self.mediaFrame.setStyleSheet("""background-color: #181818;
                                      border-radius: 12px;""")

        self.mediaLayout = QHBoxLayout(self.mediaFrame)
        # Media Player Frame Dark: #282828 White: #E6E6E6
        self.playerFrame = QFrame()
        self.playerFrame.setStyleSheet("""background-color: #282828;
                                       border-radius: 12px;""")

        # Media Playlist Frame Dark: #282828 White: #E6E6E6
        self.playlistFrame = QFrame()
        self.playlistFrame.setStyleSheet("""background-color: #282828;
                                         border-radius: 12px;""")

        self.mediaLayout.addWidget(self.playerFrame, 4)
        self.mediaLayout.addWidget(self.playlistFrame, 1)
        self.mainLayout.addWidget(self.mediaFrame, 8)

    def setupControlsBar(self):
        # Control Bar Dark: #1E1E1E White: #C9C9C9
        self.controlsFrame = QFrame()
        self.controlsFrame.setStyleSheet("""background-color: #1E1E1E;
                                         border-radius: 12px;
                                         """)
        self.mainLayout.addWidget(self.controlsFrame, 2)

    def addLabel(self, Text):
        label = QLabel(Text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label
