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
from controllers.metadata import get_artist
from icons import Icons
from core.formats import Formats

WIDTH = 1280
HEIGHT = 720


class MainUi(object):
    def __init__(self):
        # for media playback
        self.currentIndex = -1
        self.currentFile = None
        self.file_name = "No track selected"

        # shuffle for random play back
        self.shuffleList = False
        
        """
        loop modes
        - 0 loop off
        - 1 loop playlist
        - 2 loop one
        """
        self.loopMode = 0

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

        # shuffle button + connection
        self.shuffleButton = self.controlButtons(Icons.SHUFFLE)
        self.shuffleButton.clicked.connect(self.toggleShuffle)

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

        # loop button + connection
        self.loopButton = self.controlButtons(Icons.LOOP)
        self.loopButton.clicked.connect(self.toggleLoop)

        self.transportLayout.addWidget(
            self.shuffleButton, alignment=Qt.AlignmentFlag.AlignVCenter
        )
        self.transportLayout.addWidget(
            self.previousButton, alignment=Qt.AlignmentFlag.AlignVCenter
        )
        self.transportLayout.addWidget(
            self.playPauseButton, alignment=Qt.AlignmentFlag.AlignVCenter
        )
        self.transportLayout.addWidget(
            self.nextButton, alignment=Qt.AlignmentFlag.AlignVCenter
        )
        self.transportLayout.addWidget(
            self.loopButton, alignment=Qt.AlignmentFlag.AlignVCenter
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
        self.shuffleButton.setEnabled(False)
        self.previousButton.setEnabled(False)
        self.playPauseButton.setEnabled(False)
        self.nextButton.setEnabled(False)
        self.loopButton.setEnabled(False)
        self.positionSlider.setEnabled(False)

        self.mainLayout.addWidget(self.controlsFrame, 2)
        
    def toggleShuffle(self):
        self.shuffleList = not self.shuffleList
        
        if self.shuffleList:
            self.statusLabel.setText("Shuffle: On")
        else:
            self.statusLabel.setText("Shuffle: Off")
        
    def toggleLoop(self):
        self.loopMode = (self.loopMode + 1) % 3
        
        if self.loopMode == 0:
            self.statusLabel.setText("Loop: Off")
            self.loopButton.setIcon(QIcon(Icons.LOOP))
        elif self.loopMode == 1:
            self.statusLabel.setText("Loop: Playlist")
            self.loopButton.setIcon(QIcon(Icons.LOOP))
        elif self.loopMode == 2:
            self.statusLabel.setText("Loop: One")
            self.loopButton.setIcon(QIcon(Icons.LOOP_ONE))

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
        Button.setIconSize(QSize(48, 48))
        Button.setFixedSize(64, 64)
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
        self,
        text,
        font_size=20,
        bold=True,
        min_height=58,
        padding="12px 18px",
        text_color="#F2F2F2",
        bg_color="transparent",
        border_color="#E6E6E6",
    ):
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setMinimumHeight(min_height)
        weight = 700 if bold else 500
        label.setStyleSheet(f"""
            QLabel {{
                color: {text_color};
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 18px;
                font-size: {font_size}px;
                font-weight: {weight};
                padding: {padding};
            }}
        """)
        return label

    def audioOutlineButton(self, text, checkable=False):
        button = QPushButton(text)
        button.setFixedSize(64, 64)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setCheckable(checkable)
        button.setStyleSheet("""
            QPushButton {
                color: #F2F2F2;
                background-color: #181818;
                border: 2px solid #FF3344;
                border-radius: 32px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #FF3344;
                border-color: #F2F2F2;
            }
            QPushButton:checked {
                color: #FF3344;
                border-color: #FF3344;
                background-color: #121212;
            }
        """)
        return button

    # Update Icon ---- Section
    def updatePlayPauseIcon(self, state):
        current_file = self.currentFile
        if current_file is not None:
            if hasattr(current_file, "toLocalFile"):
                current_file = current_file.toLocalFile()
            current_file = str(current_file)
        self.file_name = os.path.basename(current_file) if current_file else None

        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.playPauseButton.setIcon(QIcon(Icons.PAUSE))
            if self.file_name:
                self.statusLabel.setText(f"Playing: {self.file_name}")
            else:
                self.statusLabel.setText("Playing")

        elif state == QMediaPlayer.PlaybackState.PausedState:
            self.playPauseButton.setIcon(QIcon(Icons.PLAY))
            if self.file_name:
                self.statusLabel.setText(f"Paused: {self.file_name}")
            else:
                self.statusLabel.setText("Paused")
        else:
            self.playPauseButton.setIcon(QIcon(Icons.PLAY))
            self.statusLabel.setText("Ready")

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
            "Now Playing",
            font_size=18,
            bold=True,
            min_height=46,
            padding="8px 18px",
            text_color="#FF3344",
            bg_color="#F2F2F2",
            border_color="black",
        )
        self.nowPlayingLayout.addWidget(self.nowPlayingTitle)
        self.nowPlayingLayout.addSpacing(20)

        # The star of the page — largest, boldest, tallest card
        self.songNameLabel = self.audioOutlineCard(
            self.file_name,
            font_size=28,
            bold=True,
            min_height=76,
            padding="16px 22px",
            bg_color="#181818",
            border_color="#FF3344",
        )
        self.nowPlayingLayout.addWidget(self.songNameLabel)
        self.nowPlayingLayout.addSpacing(20)

        # Subtitle — smaller and lighter than both cards above
        self.artistInfoLabel = self.audioOutlineCard(
            "Author Name: Unknown",
            font_size=15,
            bold=True,
            min_height=38,
            padding="6px 18px",
            text_color="#FF3344",
            bg_color="#F2F2F2",
            border_color="black",
        )
        self.nowPlayingLayout.addWidget(self.artistInfoLabel)
        self.nowPlayingLayout.addSpacing(14)

        self.artistButtonsLayout = QHBoxLayout()
        self.artistButtonsLayout.setSpacing(24)
        self.artistButtonsLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        
    def playRandom(self):
        count = self.playlistWidget.count()
        
        if count == 0:
            return 
        
        if count == 1:
            return 
        
        availableIndexes = [
            index for index in range(count)
            if index != self.currentIndex
        ]
        
        self.currentIndex = random.choice(availableIndexes)
        item = self.playlistWidget.item(self.currentIndex)
        self.playlistWidget.setCurrentItem(item)
        
        file_path = item.data(Qt.ItemDataRole.UserRole)
        self.playMedia(file_path)

    def mediaStatusChanged(self, status):
        if status != QMediaPlayer.MediaStatus.EndOfMedia:
            return
        
        if self.loopMode == 2:
            self.controller.mediaPlayer.setPosition(0)
            self.controller.mediaPlayer.play()
            return
        
        if self.shuffleList:
            self.playRandom()
            return
        
        if self.loopMode == 1:
            self.playNext()
            return
        
        if self.currentIndex < self.playlistWidget.count() - 1:
            self.playNext()
            
        else:
            self.controller.stop()
            

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
        self.file_name = os.path.basename(filePath)
        page = self.controller.loadMedia(filePath)

        if page == "video":
            self.playerStack.setCurrentWidget(self.videoPage)
        elif page == "audio":
            self.playerStack.setCurrentWidget(self.musicPage)
            if hasattr(self, "songNameLabel"):
                self.songNameLabel.setText(self.file_name)

            artist = get_artist(filePath)

            if hasattr(self, "artistInfoLabel"):
                self.artistInfoLabel.setText(f"Author Name: {artist}")
        else:
            QMessageBox.warning(
                self.MainWindow, "Unsupported", "Unsupported media format."
            )

        self.statusLabel.setText(f"Playing: {self.file_name}")

        self.shuffleButton.setEnabled(True)
        self.previousButton.setEnabled(True)
        self.playPauseButton.setEnabled(True)
        self.nextButton.setEnabled(True)
        self.loopButton.setEnabled(True)
        self.positionSlider.setEnabled(True)

    def setupPlaylistArea(self):
        # Playlist Section
        self.playlistFrame = QFrame()
        self.playlistFrame.setObjectName("playlistFrame")
        self.playlistFrame.setStyleSheet("""
            QFrame#playlistFrame {
                background-color: #1E1E1E;
                border-radius: 12px;
            }
        """)

        self.playlistLayout = QVBoxLayout(self.playlistFrame)
        self.playlistLayout.setContentsMargins(16, 16, 16, 14)
        self.playlistLayout.setSpacing(12)

        # ---- Header: red eyebrow label + pill-style count badge ----
        self.playlistHeaderLayout = QHBoxLayout()
        self.playlistHeaderLayout.setSpacing(8)

        self.playlistLabel = QLabel("PLAYLIST")
        playlistFont = QFont("Segoe UI", 11)
        playlistFont.setWeight(QFont.Weight.DemiBold)
        self.playlistLabel.setFont(playlistFont)
        self.playlistLabel.setStyleSheet("""
            QLabel {
              color: #FF3344;
              font-weight: 700;
              letter-spacing: 2px;
              background: transparent;
            }
        """)
        self.playlistHeaderLayout.addWidget(self.playlistLabel)
        self.playlistHeaderLayout.addStretch()

        self.playlistCountLabel = QLabel("0")
        self.playlistCountLabel.setFixedHeight(22)
        self.playlistCountLabel.setMinimumWidth(28)
        self.playlistCountLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.playlistCountLabel.setStyleSheet("""
            QLabel {
                color: #F2F2F2;
                background-color: #262626;
                border: 1px solid #3A3A3A;
                border-radius: 11px;
                padding: 0px 8px;
                font-size: 12px;
                font-weight: 600;
            }
        """)
        self.playlistHeaderLayout.addWidget(self.playlistCountLabel)
        self.playlistLayout.addLayout(self.playlistHeaderLayout)

        self.playlistDivider = QFrame()
        self.playlistDivider.setFrameShape(QFrame.Shape.HLine)
        self.playlistDivider.setStyleSheet(
            "background-color: #2A2A2A; max-height: 1px; border: none;"
        )
        self.playlistLayout.addWidget(self.playlistDivider)

        self.playlistWidget = QListWidget()
        self.playlistWidget.setSpacing(6)
        self.playlistWidget.setFrameShape(QFrame.Shape.NoFrame)

        self.playlistWidget.setIconSize(QSize(26, 26))

        self.playlistWidget.setStyleSheet("""
          QListWidget {
              background-color: transparent;
              border: none;
              outline: none;
              color: #F2F2F2;
              font-family: "Segoe UI";
              font-size: 13px;
          }

          QListWidget::item {
              background-color: #262626;
              border-left: 3px solid transparent;
              border-radius: 10px;
              padding: 10px 10px 10px 8px;
              margin: 0px;
          }

          QListWidget::item:hover {
              background-color: #2E2222;
          }

          QListWidget::item:selected {
              background-color: rgba(255, 51, 68, 30);
              color: #FF3344;
              font-weight: 600;
          }

          QListWidget::item:selected:active {
              background-color: rgba(255, 51, 68, 30);
          }

          QScrollBar:vertical {
              background: transparent;
              width: 6px;
              margin: 2px;
          }

          QScrollBar::handle:vertical {
              background: #3A3A3A;
              border-radius: 3px;
              min-height: 30px;
          }

          QScrollBar::handle:vertical:hover {
              background: #FF3344;
          }

          QScrollBar::add-line:vertical,
          QScrollBar::sub-line:vertical {
              height: 0px;
          }
                                          """)

        self.playlistWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.playlistWidget.customContextMenuRequested.connect(self.showPlaylistMenu)
        self.playlistLayout.addWidget(self.playlistWidget)
        self.playlistWidget.itemDoubleClicked.connect(self.playPlaylistItem)

    def getMediaIcon(self, file_path):

        ext = os.path.splitext(file_path)[1].lower()

        if ext in Formats.AUDIOS:
            icon_path = Icons.MUSIC

        elif ext in Formats.VIDEOS:
            icon_path = Icons.VIDEO

        else:
            return QIcon()

        pixmap = QPixmap(icon_path)

        icon = QIcon()

        icon.addPixmap(pixmap, QIcon.Mode.Normal, QIcon.State.Off)

        icon.addPixmap(pixmap, QIcon.Mode.Selected, QIcon.State.Off)

        icon.addPixmap(pixmap, QIcon.Mode.Active, QIcon.State.Off)

        icon.addPixmap(pixmap, QIcon.Mode.Disabled, QIcon.State.Off)

        return icon

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

        self.playlistCountLabel.setText(str(self.playlistWidget.count()))

    def clearPlaylist(self):

        self.controller.stop()

        self.playlistWidget.clear()
        self.playlistCountLabel.setText("0")

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
        item.setIcon(self.getMediaIcon(file_path))
        self.playlistWidget.addItem(item)

        self.playlistCountLabel.setText(str(self.playlistWidget.count()))

        return item

    def playPlaylistItem(self, item):
        self.currentIndex = self.playlistWidget.row(item)

        file_path = item.data(Qt.ItemDataRole.UserRole)
        self.playMedia(file_path)
        print("Selected playlist file:", file_path)

    def playNext(self):
        if self.playlistWidget.count() == 0:
            return
        
        if self.shuffleList:
            self.playRandom()
            return

        if self.currentIndex < self.playlistWidget.count() - 1:
            self.currentIndex += 1
        elif self.currentIndex == self.playlistWidget.count() - 1:
            if self.loopMode == 1:
                self.currentIndex = 0
            else:
                return
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
