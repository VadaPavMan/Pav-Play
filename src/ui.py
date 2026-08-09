import sys
import os
import random

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

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
from widgets.drop_area import DropArea

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
        self.setupMediaSection()

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

        # ---- Nav bar buttons ----

        # AppIcon Button
        self.navButtons("", "assets\\appicon.png")

        # OpenFile Button
        self.navButtons("Open File", "assets\\files.png")

        # OpenFolder Button
        self.navButtons("Open Folder", "assets\\folder.png")

        # ThemeToggle Button
        self.navButtons("Theme Toggle", "assets\\theme.png")

        # Settings Button
        self.navLayout.addStretch()
        self.navButtons("Settings", "assets\\settings.png")

        self.mainLayout.addWidget(self.navFrame, 1)

    def setupMediaSection(self):
        # Media Layout Dark: #181818 White: #8F8F8F
        self.mediaFrame = QFrame()
        self.mediaFrame.setStyleSheet("""background-color: #181818;
                                      border-radius: 12px;""")

        self.mediaLayout = QHBoxLayout(self.mediaFrame)
        # Media Player Frame Dark: #282828 White: #E6E6E6
        self.setupPlayerArea()
        # Media Playlist Frame Dark: #282828 White: #E6E6E6
        self.setupPlaylistArea()

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

    def navButtons(self, text, iconPath):
        Button = QPushButton(text)
        Button.setIcon(QIcon(iconPath))
        Button.setIconSize(QSize(38, 38))
        Button.setFlat(True)
        Button.setStyleSheet(
            "border: none; background: transparent; color: white; font-weight: bold;"
        )
        self.navLayout.addWidget(Button)

    def setupPlayerArea(self):
        # Media Player Frame Dark: #282828 White: #E6E6E6
        self.playerFrame = QFrame()
        self.playerFrame.setStyleSheet("""background-color: #282828;
                                       border-radius: 12px;""")
        self.playerLayout = QVBoxLayout(self.playerFrame)

        # StackedWidget() for multiple pages.
        self.playerStack = QStackedWidget()
        self.playerLayout.addWidget(self.playerStack)

        # Page 1 (Place Holder)
        self.setupPlaceholderPage()

        # Page 2 (Video Player)
        self.videoPage = QWidget()
        self.videoLayout = QVBoxLayout(self.videoPage)
        self.videoWidget = QVideoWidget()
        self.videoLayout.addWidget(self.videoWidget)
        # Will Implement it later
        self.playerStack.addWidget(self.videoPage)

        # Page 3 (Music Player)
        self.musicPage = QWidget()
        self.musicPlayerLayout = QVBoxLayout()
        self.musicPlayerLayout.addWidget(QLabel("Will Implement this later"))
        self.musicPage.setLayout(self.musicPlayerLayout)
        self.playerStack.addWidget(self.musicPage)

        self.playerStack.setCurrentIndex(0)

    def setupPlaceholderPage(self):
        self.placeHolder = QWidget()
        self.placeHolderLayout = QVBoxLayout(self.placeHolder)

        # Hero Image
        self.heroFrame = QFrame()
        self.heroLayout = QVBoxLayout(self.heroFrame)
        self.heroImage = QLabel()
        heropixmap = QPixmap("assets\\multimedia.png")
        heropixmap = heropixmap.scaled(
            150,
            150,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.heroImage.setPixmap(heropixmap)
        self.heroImage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.heroLayout.addWidget(self.heroImage)
        self.placeHolderLayout.addWidget(self.heroFrame)
        
        # Drop Media
        self.dropArea = DropArea()
        self.dropArea.fileSelected.connect(self.onFileSelected)
        self.placeHolderLayout.addWidget(self.dropArea)
        self.playerStack.addWidget(self.placeHolder)

        #

    def onFileSelected(self, filePath):
        print("Selected:", filePath)

    def setupPlaylistArea(self):
        # Media Playlist Frame Dark: #282828 White: #E6E6E6
        self.playlistFrame = QFrame()
        self.playlistFrame.setStyleSheet("""background-color: #282828;
                                                 border-radius: 12px;""")

    def addLabel(self, Text):
        label = QLabel(Text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label
