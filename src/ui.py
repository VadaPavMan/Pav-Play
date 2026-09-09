import sys
import os
import random
import time

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PySide6.QtCore import (
    QSize,
    Qt,
    QUrl,
    QTime,
    QTimer,
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
from core.link import Link
from settings.settings_page import SettingsPage
from settings.settings_manager import SettingsManager

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

        # Theme
        self.isDarkMode = True

        # Persistent application settings
        self.settingsManager = SettingsManager()

        # Session playback positions used by the Resume Playback setting.
        self._sessionPositions = {}

        # Resume requests are generation-based so an old media load can never
        # restore its position into a newly opened file.
        self._resumeRequestId = 0
        self._pendingResumeFile = None
        self._pendingResumePosition = None

        # Settings navigation
        self._previousPlayerWidget = None

        QApplication.setEffectEnabled(Qt.UI_FadeTooltip, True)

    def setup(self, MainWindow):
        self.MainWindow = MainWindow
        self.setupWindow()
        # Main Layout
        self.setupMainLayout()

        # Navigation Bar
        self.setupNavigationBar()

        # Main content stack keeps the player and Settings as mutually
        # exclusive views. This prevents the Settings page from being
        # painted underneath/alongside the player area.
        self.contentStack = QStackedWidget()
        self.contentStack.setObjectName("contentStack")
        self.contentStack.setStyleSheet(
            "QStackedWidget#contentStack { background: transparent; border: none; }"
        )
        self.playerContent = QWidget()
        self.playerContentLayout = QVBoxLayout(self.playerContent)
        self.playerContentLayout.setContentsMargins(0, 0, 0, 0)
        self.playerContentLayout.setSpacing(10)
        self.contentStack.addWidget(self.playerContent)
        self.mainLayout.addWidget(self.contentStack, 10)

        # Media Layout
        self.setupMediaSection()

        # Control Bar
        self.setupControlsBar()

        # Apply initial theme
        self.applyTheme()

    def setupWindow(self):
        if not self.MainWindow.objectName():
            self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(WIDTH, HEIGHT)

    def setupMainLayout(self):
        self.centralWidget = QWidget()
        self.centralWidget.setObjectName("centralWidget")
        # White: #1c1c1c Dark: #121212
        self.centralWidget.setStyleSheet(
            "QWidget#centralWidget { background-color: #1c1c1c; border: none; }"
        )
        self.MainWindow.setCentralWidget(self.centralWidget)
        self.mainLayout = QVBoxLayout(self.centralWidget)
        # Spacing & Margins
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(10)

    def setupNavigationBar(self):
        # White: #ecebe4 Dark: #1E1E1E
        self.navFrame = QFrame()
        self.navFrame.setObjectName("navFrame")
        self.navFrame.setStyleSheet(
            """QFrame#navFrame { background-color: #ecebe4; border: none; border-radius: 12px; }"""
        )
        self.navLayout = QHBoxLayout(self.navFrame)
        self.navLayout.setSpacing(20)

        # ---- Nav bar buttons ----

        # AppIcon Button
        self.appiconBtn = self.navButtons("", Icons.APPICON)
        self.appiconBtn.clicked.connect(lambda: Link.direct(Link.GITHUB_REPO))
        self.appiconBtn.setToolTip("Pav Play")
        self.navLayout.addWidget(self.appiconBtn)

        # OpenFile Button
        self.openfilesBtn = self.navButtons("", Icons.FILES)
        self.openfilesBtn.clicked.connect(self.openFiles)
        self.openfilesBtn.setToolTip("Files")
        self.navLayout.addWidget(self.openfilesBtn)

        # OpenFolder Button
        self.openFolderBtn = self.navButtons("", Icons.FOLDER)
        self.openFolderBtn.clicked.connect(self.openFolder)
        self.openFolderBtn.setToolTip("Folders")
        self.navLayout.addWidget(self.openFolderBtn)

        # ThemeToggle Button
        self.themeToggleBtn = self.navButtons("", Icons.THEME)
        self.themeToggleBtn.setToolTip("Light / Dark")
        self.themeToggleBtn.clicked.connect(self.toggleTheme)
        self.navLayout.addWidget(self.themeToggleBtn)

        # Settings Button
        self.navLayout.addStretch()
        self.settingsBtn = self.navButtons("", Icons.SETTINGS)
        self.settingsBtn.setToolTip("Settings")
        self.settingsBtn.clicked.connect(self.openSettings)
        self.navLayout.addWidget(self.settingsBtn)

        # Adding Buttons to layout

        self.mainLayout.addWidget(self.navFrame, 1)

    def setupMediaSection(self):
        # White: #ecebe4 Dark: #181818
        self.mediaFrame = QFrame()
        self.mediaFrame.setObjectName("mediaFrame")
        self.mediaFrame.setStyleSheet(
            """QFrame#mediaFrame { background-color: #ecebe4; border: none; border-radius: 12px; }"""
        )

        self.mediaLayout = QHBoxLayout(self.mediaFrame)
        self.setupPlayerArea()
        self.setupPlaylistArea()

        self.mediaLayout.addWidget(self.playerFrame, 4)
        self.mediaLayout.addWidget(self.playlistFrame, 1)
        self.playerContentLayout.addWidget(self.mediaFrame, 8)

    def setupControlsBar(self):

        self.controlsFrame = QFrame()
        self.controlsFrame.setObjectName("controlsFrame")
        self.controlsLayout = QVBoxLayout(self.controlsFrame)
        self.controlsLayout.setContentsMargins(15, 15, 15, 15)

        # Progress Bar (Seek Area)
        self.progressLayout = QHBoxLayout()

        self.currentTimeLabel = QLabel("0:00")
        self.currentTimeLabel.setToolTip("Duration Label")
        self.positionSlider = QSlider(Qt.Orientation.Horizontal)
        self.positionSlider.setRange(0, 1000)
        self.positionSlider.sliderMoved.connect(self.seekPosition)
        self.positionSlider.setToolTip("Seek Slider")
        self.positionSlider.setStyleSheet(self.SliderStyle())
        self.totalTimeLabel = QLabel("0:00")
        self.totalTimeLabel.setToolTip("Duration Label")

        self.progressLayout.addWidget(self.currentTimeLabel)
        self.progressLayout.addWidget(self.positionSlider)
        self.progressLayout.addWidget(self.totalTimeLabel)

        self.controlsLayout.addLayout(self.progressLayout)

        # Volume Section
        self.volumeLayout = QHBoxLayout()
        self.volumeLayout.setSpacing(8)

        self.volumeButton = self.controlButtons(Icons.SPEAKER)
        self.volumeButton.setIconSize(QSize(42, 42))
        self.volumeButton.setToolTip("Volume: Mute / UnMute")
        self.volumeButton.clicked.connect(self.toggleMute)

        # --  volume Slider
        self.volumeSlider = QSlider(Qt.Orientation.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(100)
        self.volumeSlider.setFixedWidth(120)
        self.volumeSlider.setToolTip("Volume Slider")
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
        self.shuffleButton.setToolTip("Shuffle Playback")
        self.shuffleButton.clicked.connect(self.toggleShuffle)

        # previous button + connection
        self.previousButton = self.controlButtons(Icons.PREVIOUS)
        self.previousButton.setToolTip("Previous Track")
        self.previousButton.clicked.connect(self.playPrevious)

        self.playPauseButton = self.controlButtons(Icons.PLAY)
        self.playPauseButton.setFixedSize(80, 80)
        self.playPauseButton.setIconSize(QSize(68, 68))
        self.playPauseButton.setToolTip("Play / Pause")
        self.playPauseButton.clicked.connect(self.controller.togglePlayPause)

        # next button + connection
        self.nextButton = self.controlButtons(Icons.NEXT)
        self.nextButton.setToolTip("Next Track")
        self.nextButton.clicked.connect(self.playNext)

        # loop button + connection
        self.loopButton = self.controlButtons(Icons.LOOP_OFF)  # Default Loop off
        self.loopButton.setToolTip("Loop")
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
        self.statusLabel.setToolTip("Status")
        statusFont = QFont("Segoe UI", 10)
        statusFont.setWeight(QFont.Weight.DemiBold)
        self.statusLabel.setFont(statusFont)
        self.statusLabel.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        # white: #BCBCB6 dark: #292929
        self.statusLabel.setStyleSheet("""
            QLabel {
                color: #F2F2F2;
                background-color: #BCBCB6;
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

        # White: #ecebe4 Dark: #1E1E1E
        self.controlsFrame.setStyleSheet(
            """QFrame#controlsFrame { background-color: #ecebe4; border: none; border-radius: 12px; }"""
        )

        # Initially set to disable
        self.shuffleButton.setEnabled(False)
        self.previousButton.setEnabled(False)
        self.playPauseButton.setEnabled(False)
        self.nextButton.setEnabled(False)
        self.loopButton.setEnabled(False)
        self.positionSlider.setEnabled(False)

        self.playerContentLayout.addWidget(self.controlsFrame, 2)

        # Apply persisted audio defaults.
        self.applyAudioSettings()

        # Settings is a sibling view of the player content, not another item
        # below it. The stacked container guarantees only one is visible.
        self.settingsPage = SettingsPage()
        self.settingsPage.backRequested.connect(self.closeSettings)
        self.contentStack.addWidget(self.settingsPage)

    def openSettings(self):
        if self.contentStack.currentWidget() is self.settingsPage:
            return

        self._previousPlayerWidget = self.playerStack.currentWidget()
        self.contentStack.setCurrentWidget(self.settingsPage)

    def closeSettings(self):
        if self.contentStack.currentWidget() is not self.settingsPage:
            return

        self.applyAudioSettings()
        self.contentStack.setCurrentWidget(self.playerContent)

        # A media file can be opened while Settings is visible. In that case
        # _previousPlayerWidget still points to the page that was visible when
        # Settings was opened (usually the dashboard/placeholder), so restoring
        # it would hide the newly loaded media even though playback is active.
        # Always prefer the page that matches the currently loaded media.
        if self.currentFile and os.path.isfile(self.currentFile):
            extension = os.path.splitext(self.currentFile)[1].lower()

            if extension in Formats.VIDEOS:
                self.playerStack.setCurrentWidget(self.videoPage)
            elif extension in Formats.AUDIOS:
                self.playerStack.setCurrentWidget(self.musicPage)
            elif self._previousPlayerWidget is not None:
                self.playerStack.setCurrentWidget(self._previousPlayerWidget)
        elif self._previousPlayerWidget is not None:
            self.playerStack.setCurrentWidget(self._previousPlayerWidget)


    def applyAudioSettings(self):
        """Apply persisted audio defaults to the current player session."""

        volume = self.settingsManager.get("audio/default_volume")
        try:
            volume = int(volume)
        except (TypeError, ValueError):
            volume = 100
        volume = max(0, min(100, volume))

        remember_volume = self.settingsManager.get("audio/remember_volume")
        if isinstance(remember_volume, str):
            remember_volume = remember_volume.strip().lower() in ("1", "true", "yes", "on")
        else:
            remember_volume = bool(remember_volume)

        if remember_volume:
            remembered_volume = self.settingsManager.get("audio/remembered_volume")
            try:
                if remembered_volume is not None:
                    volume = int(remembered_volume)
            except (TypeError, ValueError):
                pass
        else:
            # Avoid bringing back an old remembered value if the user
            # disables Remember Volume and later enables it again.
            self.settingsManager.settings.remove("audio/remembered_volume")

        volume = max(0, min(100, volume))

        self.volumeSlider.blockSignals(True)
        self.volumeSlider.setValue(volume)
        self.volumeSlider.blockSignals(False)
        self.controller.audioOutput.setVolume(volume / 100)
        shuffle = self.settingsManager.get("audio/default_shuffle")
        if isinstance(shuffle, str):
            shuffle = shuffle.strip().lower() in ("1", "true", "yes", "on")
        else:
            shuffle = bool(shuffle)
        self.shuffleList = shuffle

        loop_mode = self.settingsManager.get("audio/default_loop_mode")
        try:
            loop_mode = int(loop_mode)
        except (TypeError, ValueError):
            loop_mode = 0
        self.loopMode = max(0, min(2, loop_mode))

        if self.loopMode == 0:
            self.loopButton.setIcon(QIcon(Icons.LOOP_OFF))
            self.loopButton.setToolTip("Loop: Off")
        elif self.loopMode == 1:
            self.loopButton.setIcon(QIcon(Icons.LOOP))
            self.loopButton.setToolTip("Loop: Playlist")
        else:
            self.loopButton.setIcon(QIcon(Icons.LOOP_ONE))
            self.loopButton.setToolTip("Loop: One")


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
            self.loopButton.setIcon(QIcon(Icons.LOOP_OFF))
            self.loopButton.setToolTip("Loop: Off")
        elif self.loopMode == 1:
            self.statusLabel.setText("Loop: Playlist")
            self.loopButton.setIcon(QIcon(Icons.LOOP))
            self.loopButton.setToolTip("Loop: Playlist")
        elif self.loopMode == 2:
            self.statusLabel.setText("Loop: One")
            self.loopButton.setIcon(QIcon(Icons.LOOP_ONE))
            self.loopButton.setToolTip("Loop: One")

    def changeVolume(self, value):
        volume = value / 100
        self.controller.audioOutput.setVolume(volume)
        # Remember Volume stores the user's actual slider level, not the
        # muted state. The value is restored on the next application start.
        remember_volume = self.settingsManager.get("audio/remember_volume")
        if isinstance(remember_volume, str):
            remember_volume = remember_volume.strip().lower() in ("1", "true", "yes", "on")
        else:
            remember_volume = bool(remember_volume)

        if remember_volume:
            self.settingsManager.set("audio/remembered_volume", int(value))

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

    def SliderStyle(self, colors=None):
        if colors is None:
            colors = self.getThemeColors()

        return f"""
        QSlider {{
            min-height: 28px;
            background: transparent;
        }}
        QSlider::groove:horizontal {{
            height: 6px;
            background: {colors["slider_bg"]};
            border: 1px solid {colors["slider_border"]};
            border-radius: 3px;
        }}
        QSlider::sub-page:horizontal {{
            background: #FF3344;
            border: 1px solid #FF3344;
            border-radius: 3px;
        }}
        QSlider::add-page:horizontal {{
            background: {colors["slider_bg"]};
            border: 1px solid {colors["slider_border"]};
            border-radius: 3px;
        }}
        QSlider::handle:horizontal {{
            width: 18px;
            height: 18px;
            margin: -6px 0;
            background: {colors["slider_handle"]};
            border: 2px solid #FF3344;
            border-radius: 9px;
        }}
        QSlider::handle:horizontal:hover {{
            background: #FF3344;
            border: 2px solid {colors["slider_handle"]};
        }}
        QSlider::handle:horizontal:pressed {{
            background: {colors["slider_pressed"]};
            border: 2px solid #FF3344;
        }}
        """

    def controlButtons(self, iconPath):
        Button = QPushButton()
        Button.setIcon(QIcon(iconPath))
        Button.setIconSize(QSize(48, 48))
        Button.setFixedSize(64, 64)
        Button.setFlat(True)
        Button.setStyleSheet("border: none; background: transparent;")
        return Button

    def navButtons(self, text, iconPath):
        Button = QPushButton(text)
        Button.setIcon(QIcon(iconPath))
        Button.setIconSize(QSize(48, 48))
        Button.setFlat(True)
        Button.setStyleSheet("border: none; background: transparent;")
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
        button.setStyleSheet(self.audioOutlineButtonStyle())
        return button

    def audioOutlineButtonStyle(self):
        # These audio-page buttons intentionally keep the same colors in
        # both themes. They are part of the original audio-player design.
        return """
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
        """

    def getThemeColors(self):
        # Surface colors below follow the light/dark pairs specified in ui.py.
        if self.isDarkMode:
            return {
                "window": "#121212",
                "nav": "#1E1E1E",
                "media": "#181818",
                "controls": "#1E1E1E",
                "status": "#292929",
                "player": "#282828",
                "playlist": "#1E1E1E",
                "text": "#F2F2F2",
                "surface": "#262626",
                "button_hover": "#262626",
                "playlist_hover": "#2E2222",
                "checked_bg": "#121212",
                "border": "#3A3A3A",
                "divider": "#2A2A2A",
                "slider_bg": "#141414",
                "slider_border": "#000000",
                "slider_handle": "#FFFFFF",
                "slider_pressed": "#000000",
            }

        return {
            "window": "#1c1c1c",
            "nav": "#ecebe4",
            "media": "#ecebe4",
            "controls": "#ecebe4",
            "status": "#BCBCB6",
            "player": "#BCBCB6",
            "playlist": "#BCBCB6",
            "text": "#1c1c1c",
            "surface": "#D8D7D0",
            "button_hover": "#D8D7D0",
            "playlist_hover": "#E5E3DA",
            "checked_bg": "#E6E5DE",
            "border": "#8F8F8A",
            "divider": "#C4C3BC",
            "slider_bg": "#8F8F8A",
            "slider_border": "#6F6E69",
            "slider_handle": "#FFFFFF",
            "slider_pressed": "#1c1c1c",
        }

    def _interpolateColor(self, start, end, progress):
        start = start.lstrip("#")
        end = end.lstrip("#")
        sr, sg, sb = int(start[0:2], 16), int(start[2:4], 16), int(start[4:6], 16)
        er, eg, eb = int(end[0:2], 16), int(end[2:4], 16), int(end[4:6], 16)
        r = round(sr + (er - sr) * progress)
        g = round(sg + (eg - sg) * progress)
        b = round(sb + (eb - sb) * progress)
        return f"#{r:02X}{g:02X}{b:02X}"

    def _animateTheme(self):
        if not hasattr(self, "_themeStartColors"):
            return

        elapsed = time.monotonic() - self._themeAnimationStart
        progress = min(elapsed / 0.5, 1.0)

        # Smooth ease-in-out instead of a linear jump.
        progress = progress * progress * (3.0 - 2.0 * progress)

        animatedColors = {}
        for key, startColor in self._themeStartColors.items():
            targetColor = self._themeTargetColors[key]
            animatedColors[key] = self._interpolateColor(
                startColor, targetColor, progress
            )

        # Only theme-dependent widgets are restyled. The audio cards/buttons
        # intentionally remain untouched and keep their original colors.
        self.applyTheme(animatedColors, updateHero=False, animationFrame=True)

        if elapsed >= 0.5:
            self._themeTimer.stop()
            self.isDarkMode = self._themeTargetIsDark
            self.applyTheme()
            self.themeToggleBtn.setEnabled(True)

    def toggleTheme(self):
        # Smoothly interpolate the theme colors over exactly 0.5 seconds.
        # There is no opacity/fade effect on the application window.
        if hasattr(self, "_themeTimer") and self._themeTimer.isActive():
            return

        self.themeToggleBtn.setEnabled(False)

        self._themeStartColors = self.getThemeColors()
        self._themeTargetIsDark = not self.isDarkMode

        # Get the target palette without changing the active theme yet.
        self.isDarkMode = self._themeTargetIsDark
        self._themeTargetColors = self.getThemeColors()
        self.isDarkMode = not self._themeTargetIsDark

        self._themeAnimationStart = time.monotonic()

        if not hasattr(self, "_themeTimer"):
            self._themeTimer = QTimer()
            self._themeTimer.timeout.connect(self._animateTheme)

        self._themeTimer.start(25)

    def applyTheme(self, colors=None, updateHero=True, animationFrame=False):
        if colors is None:
            colors = self.getThemeColors()

        # Named selectors are intentional: styling generic QFrame/QWidget here
        # can paint over child widgets and make rounded corners look square.
        self.centralWidget.setStyleSheet(
            f"QWidget#centralWidget {{ background-color: {colors['window']}; border: none; }}"
        )
        self.navFrame.setStyleSheet(
            f"QFrame#navFrame {{ background-color: {colors['nav']}; border: none; border-radius: 12px; }}"
        )
        self.mediaFrame.setStyleSheet(
            f"QFrame#mediaFrame {{ background-color: {colors['media']}; border: none; border-radius: 12px; }}"
        )
        self.controlsFrame.setStyleSheet(
            f"QFrame#controlsFrame {{ background-color: {colors['controls']}; border: none; border-radius: 12px; }}"
        )
        self.playerFrame.setStyleSheet(
            f"QFrame#playerFrame {{ background-color: {colors['player']}; border: none; border-radius: 12px; }}"
        )
        self.playlistFrame.setStyleSheet(
            f"QFrame#playlistFrame {{ background-color: {colors['playlist']}; border: none; border-radius: 12px; }}"
        )

        if hasattr(self, "settingsPage"):
            self.settingsPage.applyTheme(colors)

        nav_style = f"""
            QPushButton {{
                border: none;
                background: transparent;
                color: {colors['text']};
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {colors['button_hover']};
                border-radius: 10px;
            }}
        """
        for button in (
            self.appiconBtn,
            self.openfilesBtn,
            self.openFolderBtn,
            self.themeToggleBtn,
            self.settingsBtn,
        ):
            button.setStyleSheet(nav_style)

        control_style = f"""
            QPushButton {{
                border: none;
                background: transparent;
                color: {colors['text']};
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {colors['button_hover']};
                border-radius: 32px;
            }}
            QPushButton:disabled {{
                background: transparent;
            }}
        """
        for button in (
            self.shuffleButton,
            self.previousButton,
            self.playPauseButton,
            self.nextButton,
            self.loopButton,
            self.volumeButton,
        ):
            button.setStyleSheet(control_style)

        self.currentTimeLabel.setStyleSheet(
            f"color: {colors['text']}; background: transparent;"
        )
        self.totalTimeLabel.setStyleSheet(
            f"color: {colors['text']}; background: transparent;"
        )

        self.statusLabel.setStyleSheet(f"""
            QLabel {{
                color: {colors['text']};
                background-color: {colors['status']};
                border: none;
                border-radius: 14px;
                padding: 7px 14px;
            }}
        """)

        self.positionSlider.setStyleSheet(self.SliderStyle(colors))
        self.volumeSlider.setStyleSheet(self.SliderStyle(colors))

        self.musicPageFrame.setStyleSheet(f"""
            QFrame#musicPageFrame {{
                background-color: transparent;
            }}
        """)
        if not animationFrame:
            self.albumArtFrame.setStyleSheet(
                "QFrame#albumArtFrame { background: transparent; border: none; }"
            )
            self.nowPlayingFrame.setStyleSheet(
                "QFrame#nowPlayingFrame { background: transparent; border: none; }"
            )

        # Audio-page cards intentionally keep the same colors in both themes.
        # Do not rebuild these styles on every animation frame. They never change.
        if not animationFrame:
            self.nowPlayingTitle.setStyleSheet("""
                QLabel {
                    color: #FF3344;
                    background-color: #ecebe4;
                    border: 2px solid #181818;
                    border-radius: 18px;
                    font-size: 18px;
                    font-weight: 700;
                    padding: 8px 18px;
                }
            """)
            self.songNameLabel.setStyleSheet("""
                QLabel {
                    color: #F2F2F2;
                    background-color: #181818;
                    border: 2px solid #FF3344;
                    border-radius: 18px;
                    font-size: 28px;
                    font-weight: 700;
                    padding: 16px 22px;
                }
            """)
            self.artistInfoLabel.setStyleSheet("""
                QLabel {
                    color: #FF3344;
                    background-color: #ecebe4;
                    border: 2px solid #181818;
                    border-radius: 18px;
                    font-size: 15px;
                    font-weight: 700;
                    padding: 6px 18px;
                }
            """)

            outline_style = self.audioOutlineButtonStyle()
            for button in (self.songButton, self.artistButton1, self.artistButton2):
                button.setStyleSheet(outline_style)

        self.playlistLabel.setStyleSheet(
            f"QLabel {{ color: #FF3344; font-weight: 700; letter-spacing: 2px; background: transparent; }}"
        )
        self.playlistCountLabel.setStyleSheet(f"""
            QLabel {{
                color: #F2F2F2;
                background-color: #262626;
                border: 1px solid #3A3A3A;
                border-radius: 11px;
                padding: 0px 8px;
                font-size: 12px;
                font-weight: 600;
            }}
        """)
        self.playlistDivider.setStyleSheet(
            "background-color: #2A2A2A; max-height: 1px; border: none;"
        )
        self.playlistWidget.setStyleSheet(f"""
          QListWidget {{
              background-color: transparent;
              border: none;
              outline: none;
              color: {colors['text']};
              font-family: "Segoe UI";
              font-size: 13px;
          }}
          QListWidget::item {{
              background-color: {colors['surface']};
              border-left: 3px solid transparent;
              border-radius: 10px;
              padding: 10px 10px 10px 8px;
              margin: 0px;
          }}
          QListWidget::item:hover {{
              background-color: {colors['playlist_hover']};
          }}
          QListWidget::item:selected {{
              background-color: rgba(255, 51, 68, 30);
              color: #FF3344;
              font-weight: 600;
          }}
          QListWidget::item:selected:active {{
              background-color: rgba(255, 51, 68, 30);
          }}
          QScrollBar:vertical {{
              background: transparent;
              width: 6px;
              margin: 2px;
          }}
          QScrollBar::handle:vertical {{
              background: {colors['border']};
              border-radius: 3px;
              min-height: 30px;
          }}
          QScrollBar::handle:vertical:hover {{
              background: #FF3344;
          }}
          QScrollBar::add-line:vertical,
          QScrollBar::sub-line:vertical {{
              height: 0px;
          }}
        """)

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
        # Do not let the backend's initial 0 ms position overwrite the saved
        # resume point while the new media is still becoming seekable.
        if self.currentFile and self._pendingResumeFile != self.currentFile:
            self._sessionPositions[self.currentFile] = position

    def updateDuration(self, duration):
        self.positionSlider.setRange(0, duration)
        self.totalTimeLabel.setText(formatTime(duration))
        # Duration can arrive before the backend is actually seekable. The
        # resume helper therefore checks both duration and seekability and also
        # retries briefly from mediaStatusChanged.
        self.restorePendingResumePosition()

    def seekPosition(self, position):
        self.controller.mediaPlayer.setPosition(position)

    def setupPlayerArea(self):

        # White: #BCBCB6 Dark: #282828
        self.playerFrame = QFrame()
        self.playerFrame.setObjectName("playerFrame")
        self.playerFrame.setStyleSheet(
            """QFrame#playerFrame { background-color: #BCBCB6; border: none; border-radius: 12px; }"""
        )
        self.playerLayout = QVBoxLayout(self.playerFrame)

        # StackedWidget() for multiple pages.
        self.playerStack = QStackedWidget()
        self.playerStack.setObjectName("playerStack")
        self.playerStack.setStyleSheet(
            "QStackedWidget#playerStack { background: transparent; border: none; }"
        )
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
        self.musicIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heroPath = Icons.MUSICHERO_G
        heroPixmap = QPixmap(heroPath)
        heroPixmap = heroPixmap.scaled(
            380,
            380,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.musicIcon.setPixmap(heroPixmap)
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
            bg_color="#282828",
            border_color="#F2F2F2",
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
            text_color="#F2F2F2",
            bg_color="#282828",
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
            bg_color="#282828",
            border_color="#F2F2F2",
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
            index for index in range(count) if index != self.currentIndex
        ]

        self.currentIndex = random.choice(availableIndexes)
        item = self.playlistWidget.item(self.currentIndex)
        self.playlistWidget.setCurrentItem(item)

        file_path = item.data(Qt.ItemDataRole.UserRole)
        self.playMedia(file_path)

    def mediaStatusChanged(self, status):
        if status in (
            QMediaPlayer.MediaStatus.LoadedMedia,
            QMediaPlayer.MediaStatus.BufferedMedia,
        ):
            self.restorePendingResumePosition()
            return

        if status != QMediaPlayer.MediaStatus.EndOfMedia:
            return

        self._pendingResumeFile = None
        self._pendingResumePosition = None

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

    def restorePendingResumePosition(self, request_id=None, attempts=40):
        """Restore a pending position only after the current media is seekable."""
        pending_file = self._pendingResumeFile
        pending_position = self._pendingResumePosition

        if pending_file is None or pending_position is None:
            return

        if request_id is not None and request_id != self._resumeRequestId:
            return

        if pending_file != self.currentFile:
            return

        player = self.controller.mediaPlayer
        duration = player.duration()

        # QMediaPlayer may report duration before it reports that the stream
        # can actually seek. Never call setPosition until both are valid.
        if duration > 0 and player.isSeekable() and 0 < pending_position < duration:
            player.setPosition(int(pending_position))
            self._pendingResumeFile = None
            self._pendingResumePosition = None
            return

        if attempts > 0:
            QTimer.singleShot(50, lambda rid=self._resumeRequestId: self.restorePendingResumePosition(
                request_id=rid, attempts=attempts - 1
            ))

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

        # Add selected file and make it the active media. This also fixes the
        # case where the playlist already contains another item: importing a
        # video should immediately display that video in the player area.
        item = self.addPlaylistItem(filePath)
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

        # Every media open creates a new resume request. This prevents an
        # asynchronous load of the previous file from affecting the new file.
        self._resumeRequestId += 1
        self._pendingResumeFile = None
        self._pendingResumePosition = None
        request_id = self._resumeRequestId

        extension = os.path.splitext(filePath)[1].lower()
        audio_exts = Formats.AUDIOS
        video_exts = Formats.VIDEOS

        if extension in audio_exts:
            resume = self.settingsManager.get("audio/resume_playback")
        elif extension in video_exts:
            resume = self.settingsManager.get("video/resume_playback")
        else:
            resume = False

        if isinstance(resume, str):
            resume = resume.strip().lower() in ("1", "true", "yes", "on")
        else:
            resume = bool(resume)

        if resume and filePath in self._sessionPositions:
            saved_position = int(self._sessionPositions[filePath])
            if saved_position > 0:
                self._pendingResumeFile = filePath
                self._pendingResumePosition = saved_position

        # Auto Play is controlled independently for audio and video.
        auto_play = True
        if extension in audio_exts:
            auto_play = self.settingsManager.get("audio/auto_play")
            if isinstance(auto_play, str):
                auto_play = auto_play.strip().lower() in ("1", "true", "yes", "on")
            else:
                auto_play = bool(auto_play)
        elif extension in video_exts:
            auto_play = self.settingsManager.get("video/auto_play")
            if isinstance(auto_play, str):
                auto_play = auto_play.strip().lower() in ("1", "true", "yes", "on")
            else:
                auto_play = bool(auto_play)

        # Switch the player area BEFORE loading/starting the media. This avoids
        # a race where QMediaPlayer starts playback while the placeholder page
        # is still visible.
        if extension in video_exts:
            self.playerStack.setCurrentWidget(self.videoPage)
        elif extension in audio_exts:
            self.playerStack.setCurrentWidget(self.musicPage)
        else:
            QMessageBox.warning(
                self.MainWindow, "Unsupported", "Unsupported media format."
            )
            return

        page = self.controller.loadMedia(filePath, auto_play=auto_play)

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
            return

        self.statusLabel.setText(f"Playing: {self.file_name}")

        self.shuffleButton.setEnabled(True)
        self.previousButton.setEnabled(True)
        self.playPauseButton.setEnabled(True)
        self.nextButton.setEnabled(True)
        self.loopButton.setEnabled(True)
        self.positionSlider.setEnabled(True)

        # Start resume asynchronously. This gives QMediaPlayer time to expose
        # a real duration/seekable state, which is important for MKV and other
        # formats whose duration is reported after the source is set.
        if self._pendingResumeFile == filePath:
            self.restorePendingResumePosition(request_id=request_id, attempts=40)

    def controllerTogglePlayPause(self):
        self.controller.togglePlayPause()

    def setupPlaylistArea(self):
        # Playlist Section
        self.playlistFrame = QFrame()
        self.playlistFrame.setObjectName("playlistFrame")
        # white: #BCBCB6 dark: #1E1E1E
        self.playlistFrame.setStyleSheet("""
            QFrame#playlistFrame {
                background-color: #BCBCB6; 
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
        item.setToolTip(f"Play: {file_name}")
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

        if not file_paths:
            return

        first_item = None
        for index, file_path in enumerate(file_paths):
            item = self.addPlaylistItem(file_path)
            if index == 0:
                first_item = item

        if first_item is not None:
            self.currentIndex = self.playlistWidget.row(first_item)
            self.playlistWidget.setCurrentItem(first_item)
            self.playMedia(first_item.data(Qt.ItemDataRole.UserRole))

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

        if not media_files:
            return

        first_item = None
        for index, file_path in enumerate(media_files):
            item = self.addPlaylistItem(file_path)
            if index == 0:
                first_item = item

        if first_item is not None:
            self.currentIndex = self.playlistWidget.row(first_item)
            self.playlistWidget.setCurrentItem(first_item)
            self.playMedia(first_item.data(Qt.ItemDataRole.UserRole))
