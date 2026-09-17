import os

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import QFileDialog, QFrame, QHBoxLayout, QLabel, QVBoxLayout
from core.formats import Formats


class DropArea(QFrame):
    fileSelected = Signal(str)
    filesSelected = Signal(list)

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

        video_formats = Formats.VIDEOS_LIST

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
        audio_formats = Formats.AUDIOS_LIST

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

    def _collectMediaFiles(self, urls):
        media_files = []
        seen = set()

        for url in urls:
            file_path = url.toLocalFile()
            if not file_path:
                continue

            file_path = os.path.abspath(file_path)

            if os.path.isfile(file_path):
                candidates = [file_path]
            elif os.path.isdir(file_path):
                try:
                    names = sorted(os.listdir(file_path))
                except OSError:
                    continue

                candidates = [os.path.join(file_path, name) for name in names]
            else:
                continue

            for candidate in candidates:
                if not os.path.isfile(candidate):
                    continue

                extension = os.path.splitext(candidate)[1].lower()
                if extension not in Formats.SUPPORTED_FORMATS_SET:
                    continue

                candidate = os.path.abspath(candidate)
                if candidate in seen:
                    continue

                seen.add(candidate)
                media_files.append(candidate)

        return media_files

    def dragEnterEvent(self, event: QDragEnterEvent):
        if not event.mimeData().hasUrls():
            event.ignore()
            return

        has_local_url = any(bool(url.toLocalFile()) for url in event.mimeData().urls())

        if has_local_url:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if not urls:
            event.ignore()
            return

        media_files = self._collectMediaFiles(urls)

        if not media_files:
            event.ignore()
            return

        self.filesSelected.emit(media_files)
        event.acceptProposedAction()

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            super().mousePressEvent(event)
            return

        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Open Media File",
            "",
            Formats.ALL_MEDIA_IMPORT,
        )

        if file_paths:
            self.filesSelected.emit(file_paths)

        event.accept()
