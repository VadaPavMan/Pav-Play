from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from ..settings_manager import SettingsManager


class VideoSettingsPage(QWidget):
    """Video playback settings."""

    def __init__(self):
        super().__init__()
        self.settings = SettingsManager()
        self.setObjectName("videoSettingsPage")

        self.titleLabel = QLabel("Video")
        self.titleLabel.setObjectName("settingsPageTitle")

        self.descriptionLabel = QLabel(
            "Configure video playback and default video behavior."
        )
        self.descriptionLabel.setObjectName("settingsPageDescription")
        self.descriptionLabel.setWordWrap(True)

        self.playbackFrame = QFrame()
        self.playbackFrame.setObjectName("videoSettingsSection")

        self.playbackTitle = QLabel("Playback")
        self.playbackTitle.setObjectName("settingsSectionTitle")

        self.autoPlayCheck = QCheckBox("Automatically play video when opened")
        self.autoPlayCheck.setCursor(Qt.CursorShape.PointingHandCursor)
        self.autoPlayCheck.toggled.connect(
            lambda checked: self.settings.set("video/auto_play", checked)
        )

        self.resumePlaybackCheck = QCheckBox(
            "Resume video playback from the previous position"
        )
        self.resumePlaybackCheck.setCursor(Qt.CursorShape.PointingHandCursor)
        self.resumePlaybackCheck.toggled.connect(
            lambda checked: self.settings.set("video/resume_playback", checked)
        )

        playbackLayout = QVBoxLayout(self.playbackFrame)
        playbackLayout.setContentsMargins(18, 16, 18, 16)
        playbackLayout.setSpacing(14)
        playbackLayout.addWidget(self.playbackTitle)
        playbackLayout.addWidget(self.autoPlayCheck)
        playbackLayout.addWidget(self.resumePlaybackCheck)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)
        layout.addWidget(self.titleLabel)
        layout.addWidget(self.descriptionLabel)
        layout.addSpacing(6)
        layout.addWidget(self.playbackFrame)
        layout.addStretch()

        self._loadSettings()

    @staticmethod
    def _toBool(value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in ("1", "true", "yes", "on")
        return bool(value)

    def _loadSettings(self):
        self.autoPlayCheck.setChecked(
            self._toBool(self.settings.get("video/auto_play"))
        )
        self.resumePlaybackCheck.setChecked(
            self._toBool(self.settings.get("video/resume_playback"))
        )

    def applyTheme(self, colors):
        text = colors["text"]
        secondary = colors.get("secondary_text", text)
        border = colors["border"]
        media = colors["media"]
        hover = colors.get("hover", media)

        self.setStyleSheet(f"""
            QWidget#videoSettingsPage {{
                background: transparent;
                border: none;
            }}
            QLabel#settingsPageTitle {{
                color: {text};
                font-size: 28px;
                font-weight: 700;
                background: transparent;
            }}
            QLabel#settingsPageDescription {{
                color: {secondary};
                font-size: 14px;
                background: transparent;
            }}
            QFrame#videoSettingsSection {{
                background-color: {media};
                border: 1px solid {border};
                border-radius: 12px;
            }}
            QLabel#settingsSectionTitle {{
                color: {text};
                font-size: 18px;
                font-weight: 700;
                background: transparent;
            }}
            QLabel#settingsOptionLabel {{
                color: {text};
                font-size: 15px;
                background: transparent;
            }}
            QCheckBox {{
                color: {text};
                font-size: 15px;
                background: transparent;
                spacing: 10px;
            }}
            QCheckBox:hover {{
                color: #FF3344;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 1px solid {border};
                border-radius: 4px;
                background: {hover};
            }}
            QCheckBox::indicator:checked {{
                background: #FF3344;
                border-color: #FF3344;
            }}
        """)
