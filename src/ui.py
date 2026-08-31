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
    QPainter,
    QPen,
    QBrush,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
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
    QGraphicsDropShadowEffect,
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from widgets.drop_area import DropArea
from controllers.player_controller import PlayerController
from controllers.formatTime import formatTime
from icons import Icons
from core.formats import Formats

WIDTH = 1280
HEIGHT = 720


class MainUi(object):
    def __init__(self):
        # for media playback
        self.currentIndex = -1

        self.currentFile = None

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
        self.appiconBtn = self.navButtons("", Icons.APPICON)
        self.navLayout.addWidget(self.appiconBtn)

        # OpenFile Button
        self.openfilesBtn = self.navButtons("", Icons.FILES)
        self.openfilesBtn.clicked.connect(self.openFiles)
        self.navLayout.addWidget(self.openfilesBtn)

        # OpenFolder Button
        self.openFolderBtn = self.navButtons("", Icons.FOLDER)
        self.openFolderBtn.clicked.connect(self.openFolder)
        self.navLayout.addWidget(self.openFolderBtn)

        # ThemeToggle Button
        self.themeToggleBtn = self.navButtons("", Icons.THEME)
        self.navLayout.addWidget(self.themeToggleBtn)

        # Settings Button
        self.navLayout.addStretch()
        self.settingsBtn = self.navButtons("", Icons.SETTINGS)
        self.navLayout.addWidget(self.settingsBtn)

        # Adding Buttons to layout

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

        # Volume Section
        self.volumeLayout = QHBoxLayout()
        self.volumeLayout.setSpacing(8)

        self.volumeButton = self.controlButtons(Icons.SPEAKER)
        self.volumeButton.setIconSize(QSize(42, 42))
        self.volumeButton.clicked.connect(self.toggleMute)

        # --  volume Slider
        self.volumeSlider = QSlider(Qt.Orientation.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(100)
        self.volumeSlider.setFixedWidth(120)
        self.volumeSlider.valueChanged.connect(self.changeVolume)

        self.volumeLayout.addWidget(
            self.volumeButton, alignment=Qt.AlignmentFlag.AlignVCenter
        )
        self.volumeLayout.addWidget(
            self.volumeSlider, alignment=Qt.AlignmentFlag.AlignVCenter
        )

        # Slider stylesheet
        self.volumeSlider.setStyleSheet(self.SliderStyle())

        # Buttons Section + Connection
        self.bottomLayout = QGridLayout()
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

        self.transportLayout.addWidget(
            self.previousButton, alignment=Qt.AlignmentFlag.AlignVCenter
        )
        self.transportLayout.addWidget(
            self.playPauseButton, alignment=Qt.AlignmentFlag.AlignVCenter
        )
        self.transportLayout.addWidget(
            self.nextButton, alignment=Qt.AlignmentFlag.AlignVCenter
        )

        # Status
        self.statusLabel = QLabel("Ready")
        statusFont = QFont("Segoe UI", 10)
        statusFont.setWeight(QFont.Weight.DemiBold)
        self.statusLabel.setFont(statusFont)
        self.statusLabel.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.statusLabel.setStyleSheet("""
            QLabel {
                color: #F2F2F2;
                background-color: #292929;
                border: 2px;
                border-radius: 14px;
                padding: 7px 14px;
            }
        """)
        self.bottomLayout.addLayout(self.volumeLayout, 0, 0, Qt.AlignmentFlag.AlignLeft)
        self.bottomLayout.addLayout(
            self.transportLayout, 0, 1, Qt.AlignmentFlag.AlignCenter
        )
        self.bottomLayout.addWidget(self.statusLabel, 0, 2, Qt.AlignmentFlag.AlignRight)
        self.bottomLayout.setColumnStretch(0, 1)
        self.bottomLayout.setColumnStretch(2, 1)

        self.controlsLayout.addLayout(self.bottomLayout)

        # Control Bar Dark: #1E1E1E White: #C9C9C9
        self.controlsFrame.setStyleSheet("""background-color: #1E1E1E;
                                         border-radius: 12px;""")

        # Initially set to disable
        self.previousButton.setEnabled(False)
        self.playPauseButton.setEnabled(False)
        self.nextButton.setEnabled(False)
        self.positionSlider.setEnabled(False)

        self.mainLayout.addWidget(self.controlsFrame, 2)

    def changeVolume(self, value):
        volume = value / 100
        self.controller.audioOutput.setVolume(volume)

        if self.controller.audioOutput.isMuted():
            self.controller.audioOutput.setMuted(False)
            self.volumeButton.setIcon(QIcon(Icons.SPEAKER))

    def toggleMute(self):
        muted = self.controller.audioOutput.isMuted()

        self.controller.audioOutput.setMuted(not muted)

        if muted:
            self.volumeButton.setIcon(QIcon(Icons.SPEAKER))
        else:
            self.volumeButton.setIcon(QIcon(Icons.MUTE))

    def SliderStyle(self):
        return """
        QSlider {
            min-height: 28px;
            background: transparent;
        }
        QSlider::groove:horizontal {
            height: 6px;
            background: #141414;
            border: 1px solid #000000;
            border-radius: 3px;
        }
        QSlider::sub-page:horizontal {
            background: #FF3344;
            border: 1px solid #000000;
            border-radius: 3px;
        }
        QSlider::add-page:horizontal {
            background: #141414;
            border: 1px solid #000000;
            border-radius: 3px;
        }
        QSlider::handle:horizontal {
            width: 18px;
            height: 18px;
            margin: -6px 0;
            background: #FFFFFF;
            border: 2px solid #FF3344;
            border-radius: 9px;
        }
        QSlider::handle:horizontal:hover {
            background: #FF3344;
            border: 2px solid #FFFFFF;
        }
        QSlider::handle:horizontal:pressed {
            background: #000000;
            border: 2px solid #FF3344;
        }
        """

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
        return Button

    def audioOutlineCard(
        self, text, font_size=20, bold=True, min_height=58, padding="12px 18px"
    ):
        # Outlined, transparent rounded-rect label used for Now Playing /
        # Song Name / Author Name on the audio page (wireframe-style cards).
        # Size/weight vary per card to create a clear visual hierarchy:
        # Song Name is the star (largest), Now Playing is a header label,
        # Author Name is a smaller subtitle.
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setMinimumHeight(min_height)
        weight = 700 if bold else 500
        label.setStyleSheet(f"""
            QLabel {{
                color: #F2F2F2;
                background-color: transparent;
                border: 2px solid #E6E6E6;
                border-radius: 18px;
                font-size: {font_size}px;
                font-weight: {weight};
                padding: {padding};
            }}
        """)
        return label

    def audioOutlineButton(self, text, checkable=False):
        # Outlined circular ghost button used for the row of action buttons
        # (like, add to playlist, more) beneath the audio page cards
        button = QPushButton(text)
        button.setFixedSize(64, 64)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setCheckable(checkable)
        button.setStyleSheet("""
            QPushButton {
                color: #F2F2F2;
                background-color: transparent;
                border: 2px solid #E6E6E6;
                border-radius: 32px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #FF3344;
                border-color: #FF3344;
            }
            QPushButton:checked {
                color: #FF3344;
                border-color: #FF3344;
                background-color: rgba(255, 51, 68, 35);
            }
        """)
        return button

    # Update Icon ---- Section
    def updatePlayPauseIcon(self, state):
        file_name = os.path.basename(self.currentFile) if self.currentFile else None

        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.playPauseButton.setIcon(QIcon(Icons.PAUSE))

            if file_name:
                self.statusLabel.setText(f"Playing: {file_name}")

        elif state == QMediaPlayer.PlaybackState.PausedState:
            self.playPauseButton.setIcon(QIcon(Icons.PLAY))

            if file_name:
                self.statusLabel.setText(f"Paused: {file_name}")
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

        # Page 3 (Audio Player)
        self.musicPage = QWidget()
        self.musicPageOuterLayout = QVBoxLayout(self.musicPage)
        self.musicPageOuterLayout.setContentsMargins(0, 0, 0, 0)

        # One big outlined card wraps the whole audio page (hero + info)
        self.musicPageFrame = QFrame()
        self.musicPageFrame.setObjectName("musicPageFrame")
        self.musicPageFrame.setStyleSheet("""
            QFrame#musicPageFrame {
                background-color: transparent;
                border: 2px solid #3A3A3A;
                border-radius: 28px;
            }
        """)
        self.musicPlayerLayout = QHBoxLayout(self.musicPageFrame)
        self.musicPlayerLayout.setContentsMargins(40, 40, 40, 40)
        self.musicPlayerLayout.setSpacing(30)
        self.musicPageOuterLayout.addWidget(self.musicPageFrame)

        # ---- Left: Hero Illustration ----
        self.albumArtFrame = QFrame()
        self.albumArtFrame.setObjectName("albumArtFrame")
        self.albumArtFrame.setStyleSheet("background: transparent; border: none;")
        self.albumArtLayout = QVBoxLayout(self.albumArtFrame)
        self.albumArtLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.musicIcon = QLabel()
        heroPixmap = QPixmap(Icons.MUSICHERO_DARK)
        heroPixmap = heroPixmap.scaled(
            380,
            380,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.musicIcon.setPixmap(heroPixmap)
        self.musicIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.albumArtLayout.addWidget(self.musicIcon)

        # ---- Right: Now Playing / Song Name / Author Name cards ----
        self.nowPlayingFrame = QFrame()
        self.nowPlayingFrame.setObjectName("nowPlayingFrame")
        self.nowPlayingFrame.setStyleSheet("background: transparent; border: none;")
        self.nowPlayingLayout = QVBoxLayout(self.nowPlayingFrame)
        self.nowPlayingLayout.setSpacing(0)
        self.nowPlayingLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # Header label — small, so it doesn't compete with the song title
        self.nowPlayingTitle = self.audioOutlineCard(
            "Now Playing", font_size=18, bold=True, min_height=46, padding="8px 18px"
        )
        self.nowPlayingLayout.addWidget(self.nowPlayingTitle)
        self.nowPlayingLayout.addSpacing(20)

        # The star of the page — largest, boldest, tallest card
        self.songNameLabel = self.audioOutlineCard(
            "Song Name (Title)",
            font_size=28,
            bold=True,
            min_height=76,
            padding="16px 22px",
        )
        self.nowPlayingLayout.addWidget(self.songNameLabel)
        self.nowPlayingLayout.addSpacing(20)

        # Subtitle — smaller and lighter than both cards above
        self.artistInfoLabel = self.audioOutlineCard(
            "Author Name", font_size=15, bold=False, min_height=38, padding="6px 18px"
        )
        self.nowPlayingLayout.addWidget(self.artistInfoLabel)
        self.nowPlayingLayout.addSpacing(14)

        # Row of circular action buttons (like, add to playlist, more) —
        # grouped closer to Author Name than the gaps between the cards above
        self.artistButtonsLayout = QHBoxLayout()
        self.artistButtonsLayout.setSpacing(16)
        self.artistButtonsLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.songButton = self.audioOutlineButton("♥", checkable=True)
        self.artistButton1 = self.audioOutlineButton("+")
        self.artistButton2 = self.audioOutlineButton("⋮")

        self.artistButtonsLayout.addWidget(self.songButton)
        self.artistButtonsLayout.addWidget(self.artistButton1)
        self.artistButtonsLayout.addWidget(self.artistButton2)

        self.nowPlayingLayout.addLayout(self.artistButtonsLayout)

        self.musicPlayerLayout.addWidget(self.albumArtFrame, 4)
        self.musicPlayerLayout.addWidget(self.nowPlayingFrame, 3)
        self.playerStack.addWidget(self.musicPage)

        # Media Setup Controller (Default Video Player)
        self.controller = PlayerController(self.videoWidget)

        # Media Control Activity
        self.controller.mediaPlayer.playbackStateChanged.connect(
            self.updatePlayPauseIcon
        )
        self.controller.mediaPlayer.positionChanged.connect(self.updatePosition)
        self.controller.mediaPlayer.durationChanged.connect(self.updateDuration)

        self.controller.mediaPlayer.mediaStatusChanged.connect(self.mediaStatusChanged)

        self.playerStack.setCurrentIndex(0)

    def mediaStatusChanged(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.playNext()

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

    # File Selection + Sets Page According to Media Format...
    def onFileSelected(self, filePath):
        print("Selected:", filePath)

        if not os.path.isfile(filePath):
            return

        # Add selected files to playlist
        item = self.addPlaylistItem(filePath)
        if self.currentIndex == -1:
            self.currentIndex = self.playlistWidget.row(item)
            self.playlistWidget.setCurrentItem(item)
            self.playMedia(filePath)

    # will you it later
    def addFilesToPlaylist(self, file_paths):
        for files in file_paths:
            self.addPlaylistItem(files)

    def playMedia(self, filePath):
        self.currentFile = filePath
        page = self.controller.loadMedia(filePath)

        if page == "video":
            self.playerStack.setCurrentWidget(self.videoPage)
        elif page == "audio":
            self.playerStack.setCurrentWidget(self.musicPage)
        else:
            QMessageBox.warning(
                self.MainWindow, "Unsupported", "Unsupported media format."
            )

        file_name = os.path.basename(filePath)
        self.statusLabel.setText(f"Playing: {file_name}")

        self.previousButton.setEnabled(True)
        self.playPauseButton.setEnabled(True)
        self.nextButton.setEnabled(True)
        self.positionSlider.setEnabled(True)

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
        self.playlistWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.playlistWidget.customContextMenuRequested.connect(self.showPlaylistMenu)

        self.playlistLayout.addWidget(self.playlistWidget)
        self.playlistWidget.itemDoubleClicked.connect(self.playPlaylistItem)

    def showPlaylistMenu(self, position):
        item = self.playlistWidget.itemAt(position)

        if item is None:
            return

        menu = QMenu(self.MainWindow)
        playAction = menu.addAction("Play")
        removeAction = menu.addAction("Remove")

        menu.addSeparator()

        clearAction = menu.addAction("Clear Playlist")

        action = menu.exec(self.playlistWidget.mapToGlobal(position))

        if action == playAction:
            self.playPlaylistItem(item)
        elif action == removeAction:
            self.removePlaylistItem(item)
        elif action == clearAction:
            self.clearPlaylist()

    def removePlaylistItem(self, item):

        row = self.playlistWidget.row(item)

        if row == self.currentIndex:
            return

        self.playlistWidget.takeItem(row)

        if row < self.currentIndex:
            self.currentIndex -= 1

    def clearPlaylist(self):

        self.controller.stop()

        self.playlistWidget.clear()

        self.currentIndex = -1
        self.currentFile = None

        self.playerStack.setCurrentIndex(0)

        self.previousButton.setEnabled(False)
        self.playPauseButton.setEnabled(False)
        self.nextButton.setEnabled(False)
        self.positionSlider.setEnabled(False)

        self.positionSlider.setValue(0)
        self.currentTimeLabel.setText("0:00")
        self.totalTimeLabel.setText("0:00")

        self.statusLabel.setText("Ready")

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

    def openFiles(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self.MainWindow,
            "Open Media File",
            "",
            Formats.ALL_MEDIA_IMPORT,
        )

        for file_path in file_paths:
            self.onFileSelected(file_path)

    def openFolder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self.MainWindow, "Select Media Folder"
        )

        if not folder_path:
            return

        media_files = []

        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            if not os.path.isfile(file_path):
                continue

            extension = os.path.splitext(file_name)[1].lower()

            if extension in Formats.SUPPORTED_FORMATS_SET:
                media_files.append(file_path)

        for file_path in media_files:
            self.onFileSelected(file_path)
