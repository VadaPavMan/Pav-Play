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
from core.formats import Formats


class PlayerController:
    def __init__(self, videoWidget):
        # Media Player Setup
        self.mediaPlayer = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        self.mediaPlayer.setVideoOutput(videoWidget)
        Formats.setMultiMediaBackend
        
    # IMP
    def loadMedia(self, filePath):
        extension = os.path.splitext(filePath)[1].lower()
        video_exts = Formats.VIDEOS
        audio_exts = Formats.AUDIOS

        if extension in video_exts:
            page = "video"
        elif extension in audio_exts:
            page = "audio"
        else:
            return None

        self.mediaPlayer.setSource(QUrl.fromLocalFile(filePath))
        self.mediaPlayer.play()

        return page

    def play(self):
        self.mediaPlayer.play()

    def pause(self):
        self.mediaPlayer.pause()
        
    def togglePlayPause(self):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
