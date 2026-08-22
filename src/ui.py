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
from controllers.player_controller import PlayerController
from controllers.formatTime import formatTime
from icons import Icons

WIDTH = 1280
HEIGHT = 720


class MainUi(object):
    def __init__(self):
        # for media playback
        self.currentIndex = -1

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
        self.navButtons("", Icons.APPICON)

        # OpenFile Button
        self.navButtons("", Icons.FILES)

        # OpenFolder Button
        self.navButtons("", Icons.FOLDER)

        # ThemeToggle Button
        self.navButtons("", Icons.THEME)

        # Settings Button
        self.navLayout.addStretch()
        self.navButtons("", Icons.SETTINGS)

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

        self.controlsFrame = QFrame()
        self.controlsLayout = QVBoxLayout(self.controlsFrame)
        self.controlsLayout.setContentsMargins(15, 15, 15, 15)

        # Progress Bar (Seek Area)
        self.progressLayout = QHBoxLayout()

        self.currentTimeLabel = QLabel("0:00")
        self.positionSlider = QSlider(Qt.Orientation.Horizontal)
        self.positionSlider.setRange(0, 1000)
        self.positionSlider.sliderMoved.connect(self.seekPosition)
        self.positionSlider.setStyleSheet(self.SliderStyle())
        self.totalTimeLabel = QLabel("0:00")

        self.progressLayout.addWidget(self.currentTimeLabel)
        self.progressLayout.addWidget(self.positionSlider)
        self.progressLayout.addWidget(self.totalTimeLabel)

        self.controlsLayout.addLayout(self.progressLayout)

        # Buttons Section + Connection
        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setContentsMargins(0, 5, 0, 0)

        self.transportLayout = QHBoxLayout()
        self.transportLayout.setSpacing(12)

        # previous button + connection
        self.previousButton = self.controlButtons(Icons.PREVIOUS)
        self.previousButton.clicked.connect(self.playPrevious)

        self.playPauseButton = self.controlButtons(Icons.PLAY)
        self.playPauseButton.setFixedSize(80, 80)
        self.playPauseButton.setIconSize(QSize(68, 68))
        self.playPauseButton.clicked.connect(self.controller.togglePlayPause)

        # next button + connection
        self.nextButton = self.controlButtons(Icons.NEXT)
        self.nextButton.clicked.connect(self.playNext)

        self.transportLayout.addWidget(self.previousButton)
        self.transportLayout.addWidget(self.playPauseButton)
        self.transportLayout.addWidget(self.nextButton)

        self.bottomLayout.addStretch()

        self.bottomLayout.addLayout(self.transportLayout)

        self.bottomLayout.addStretch()

        # Volume Section
        self.volumeLayout = QHBoxLayout()
        self.volumeLayout.setSpacing(8)

        self.volumeButton = self.controlButtons(Icons.SPEAKER)
        self.volumeButton.setIconSize(QSize(42, 42))

        # -- Slider
        self.volumeSlider = QSlider(Qt.Orientation.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(100)
        self.volumeSlider.setFixedWidth(120)

        self.volumeLayout.addWidget(self.volumeButton)
        self.volumeLayout.addWidget(self.volumeSlider)

        # Slider stylesheet
        self.volumeSlider.setStyleSheet(self.SliderStyle())

        self.bottomLayout.addLayout(self.volumeLayout)

        # Status
        self.statusLabel = QLabel("Ready")
        self.statusLabel.setStyleSheet("color: #CCCCCC; font-size: 12px;")
        self.bottomLayout.addSpacing(15)
        self.bottomLayout.addWidget(self.statusLabel)

        self.controlsLayout.addLayout(self.bottomLayout)

        # Control Bar Dark: #1E1E1E White: #C9C9C9
        self.controlsFrame.setStyleSheet("""background-color: #1E1E1E;
                                         border-radius: 12px;""")

        self.mainLayout.addWidget(self.controlsFrame, 2)

    def SliderStyle(self):
        return """QSlider::groove:horizontal {
                                             height: 4px;
                                             background: #3A3A3A;
                                             border-radius: 2px;
                                         }
                                         
                                         QSlider::handle:horizontal {
                                             background: white;
                                             width: 14px;
                                             margin: -5px 0;
                                             border-radius: 7px;
                                         }"""

    def controlButtons(self, iconPath):
        Button = QPushButton()
        Button.setIcon(QIcon(iconPath))
        Button.setIconSize(QSize(42, 42))
        Button.setFixedSize(62, 62)
        Button.setFlat(True)
        Button.setStyleSheet(
            "border: none; background: transparent; color: white; font-weight: bold;"
        )
        return Button

    def navButtons(self, text, iconPath):
        Button = QPushButton(text)
        Button.setIcon(QIcon(iconPath))
        Button.setIconSize(QSize(48, 48))
        Button.setFlat(True)
        Button.setStyleSheet(
            "border: none; background: transparent; color: white; font-weight: bold;"
        )
        self.navLayout.addWidget(Button)

    # Update Icon ---- Section
    def updatePlayPauseIcon(self, state):
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.playPauseButton.setIcon(QIcon(Icons.PAUSE))
        else:
            self.playPauseButton.setIcon(QIcon(Icons.PLAY))

    # Update Section
    def updatePosition(self, position):
        self.positionSlider.blockSignals(True)
        self.positionSlider.setValue(position)
        self.positionSlider.blockSignals(False)

        self.currentTimeLabel.setText(formatTime(position))

    def updateDuration(self, duration):
        self.positionSlider.setRange(0, duration)
        self.totalTimeLabel.setText(formatTime(duration))

    def seekPosition(self, position):
        self.controller.mediaPlayer.setPosition(position)

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
        self.playerStack.addWidget(self.videoPage)

        # Page 3 (Music Player)
        self.musicPage = QWidget()
        self.musicPlayerLayout = QVBoxLayout(self.musicPage)
        self.musicPlayerLayout.addWidget(QLabel("Audio Player"))
        self.playerStack.addWidget(self.musicPage)

        # Media Setup Controller (Default Video Player)
        self.controller = PlayerController(self.videoWidget)

        # Media Control Activity
        self.controller.mediaPlayer.playbackStateChanged.connect(
            self.updatePlayPauseIcon
        )
        self.controller.mediaPlayer.positionChanged.connect(self.updatePosition)
        self.controller.mediaPlayer.durationChanged.connect(self.updateDuration)

        self.playerStack.setCurrentIndex(0)

    def setupPlaceholderPage(self):
        self.placeHolder = QWidget()
        self.placeHolderLayout = QVBoxLayout(self.placeHolder)

        # Hero Image
        self.heroFrame = QFrame()
        self.heroLayout = QVBoxLayout(self.heroFrame)
        self.heroImage = QLabel()
        heropixmap = QPixmap(Icons.MULTIMEDIA)
        heropixmap = heropixmap.scaled(
            250,
            250,
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

    # Sets Page According to Media Format...
    def onFileSelected(self, filePath):
        print("Selected:", filePath)

        # Add selected files to playlist
        item = self.addPlaylistItem(filePath)
        self.playlistWidget.setCurrentItem(item)
        self.currentIndex = self.playlistWidget.row(item)
        self.playMedia(filePath)

    def playMedia(self, filePath):
        page = self.controller.loadMedia(filePath)

        if page == "video":
            self.playerStack.setCurrentWidget(self.videoPage)
        elif page == "audio":
            self.playerStack.setCurrentWidget(self.musicPage)
        else:
            QMessageBox.warning(
                self.MainWindow, "Unsupported", "Unsupported media format."
            )

    def setupPlaylistArea(self):
        # Playlist Section
        self.playlistFrame = QFrame()
        # Media Playlist Frame Dark: #282828 White: #E6E6E6
        self.playlistFrame.setStyleSheet("""background-color: #282828;
                                           border-radius: 12px;""")

        self.playlistLayout = QVBoxLayout(self.playlistFrame)
        self.playlistLayout.setContentsMargins(10, 10, 10, 10)

        self.playlistLabel = QLabel("Play List")
        self.playlistLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.playlistLayout.addWidget(self.playlistLabel)

        self.playlistWidget = QListWidget()
        self.playlistWidget.setStyleSheet("""
                                    QListWidget {
                                        background-color: #282828;
                                        border: none;
                                        color: white;
                                        font-size: 14px;
                                    }
                                    
                                    QListWidget::item {
                                        padding: 10px;
                                        border-radius: 6px;
                                    }
                                    
                                    QListWidget::item:selected {
                                        background-color: #3A3A3A;
                                    }
                                    
                                    QListWidget::item:hover {
                                        background-color: #333333;
                                    }
                                """)

        self.playlistLayout.addWidget(self.playlistWidget)
        self.playlistWidget.itemDoubleClicked.connect(self.playPlaylistItem)

    def addPlaylistItem(self, file_path):
        # Check Duplicates
        for index in range(self.playlistWidget.count()):
            item = self.playlistWidget.item(index)
            checkFile = item.data(Qt.ItemDataRole.UserRole)

            if checkFile == file_path:
                return item

        file_name = os.path.basename(file_path)

        item = QListWidgetItem(file_name)
        item.setData(Qt.ItemDataRole.UserRole, file_path)
        self.playlistWidget.addItem(item)

        return item

    def playPlaylistItem(self, item):
        self.currentIndex = self.playlistWidget.row(item)

        file_path = item.data(Qt.ItemDataRole.UserRole)
        self.playMedia(file_path)
        print("Selected playlist file:", file_path)

    def playNext(self):
        if self.playlistWidget.count() == 0:
            return

        if self.currentIndex < self.playlistWidget.count() - 1:
            self.currentIndex += 1
        elif self.currentIndex == self.playlistWidget.count() - 1:
            self.currentIndex = 0
        else:
            return

        item = self.playlistWidget.item(self.currentIndex)
        self.playlistWidget.setCurrentItem(item)
        file_path = item.data(Qt.ItemDataRole.UserRole)
        self.playMedia(file_path)

    def playPrevious(self):
        if self.playlistWidget.count() == 0:
            return

        if self.currentIndex > 0:
            self.currentIndex -= 1
        elif self.currentIndex == 0:
            self.currentIndex = self.playlistWidget.count() - 1
        else:
            return

        item = self.playlistWidget.item(self.currentIndex)
        self.playlistWidget.setCurrentItem(item)
        file_path = item.data(Qt.ItemDataRole.UserRole)
        self.playMedia(file_path)
