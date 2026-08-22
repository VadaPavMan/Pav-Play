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
    Signal,
    QObject,
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


class DropArea(QFrame):
    fileSelected = Signal(str)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

        self.mainLayout = QVBoxLayout(self)

        self.TitleLable = QLabel("Drag & Drop Media File Here")
        self.TitleLable.setContentsMargins(50, 30, 50, 30)
        self.TitleLable.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.TitleLable)

        # Video Format HBox
        self.formatsLayout = QHBoxLayout()
        self.videoFrame = QFrame()
        self.videoFrame.setObjectName("formatCard")

        self.videoLayout = QVBoxLayout(self.videoFrame)
        self.videoLayout.setContentsMargins(15, 15, 15, 15)
        self.videoLayout.setSpacing(6)

        self.videoTitle = QLabel("Supported Video Formats")
        self.videoTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.videoLayout.addWidget(self.videoTitle)

        video_formats = ["mp4", "mkv", "mov", "webm", "avi", "wmv"]

        for fmt in video_formats:
            label = QLabel(f"• {fmt}")
            self.videoLayout.addWidget(label)

        # Audio Format HBox
        self.audioFrame = QFrame()
        self.audioFrame.setObjectName("formatCard")

        self.audioLayout = QVBoxLayout(self.audioFrame)
        self.audioLayout.setContentsMargins(15, 15, 15, 15)
        self.audioLayout.setSpacing(6)

        self.audioTitle = QLabel("Supported Audio Formats")
        self.audioTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.audioLayout.addWidget(self.audioTitle)
        audio_formats = ["mp3", "m4a", "aac", "wav", "flac", "ogg", "wma"]

        for fmt in audio_formats:
            label = QLabel(f"• {fmt}")
            self.audioLayout.addWidget(label)

        self.formatsLayout.addWidget(self.videoFrame)
        self.formatsLayout.addWidget(self.audioFrame)
        self.mainLayout.addLayout(self.formatsLayout)

        # styling
        self.styling()

    def styling(self):
        self.TitleLable.setStyleSheet("""QLabel{
            border:2px dashed gray;
            border-radius:15px;
            background:#303030;
            font-weight: bold;
            font-size: 18px;
            color: white;
            }
            """)

        self.videoTitle.setStyleSheet("font-size: 18px;")
        self.audioTitle.setStyleSheet("font-size: 18px;")

        self.setStyleSheet(
            """ QFrame { background: #1E1E1E; border: 2px solid; border-radius: 18px; } QFrame#formatCard { background: #303030; border: 2px solid; border-radius: 14px; } QLabel { color: white; background: transparent; border: none; font-weight: bold; } """
        )

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if not urls:
            return

        for url in urls:
            file_path = url.toLocalFile()

            if os.path.isfile(file_path):
                self.fileSelected.emit(file_path)
                print(file_path)

        event.acceptProposedAction()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            file_paths, _ = QFileDialog.getOpenFileNames(
                self,
                "Open Media File",
                "",
                "Media Files (*.mp3 *.m4a *.aac *.wav *.flac *.ogg *.wma *.mp4 *.mkv *.webm *.avi *.mov *.wmv);; All Files (*.*)",
            )

            for file_path in file_paths:
                self.fileSelected.emit(file_path)
        else:
            super().mousePressEvent(event)
