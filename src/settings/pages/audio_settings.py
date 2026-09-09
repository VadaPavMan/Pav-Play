from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QFormLayout, QFrame, QHBoxLayout,
    QLabel, QSlider, QVBoxLayout, QWidget,
)

from ..settings_manager import SettingsManager


class AudioSettingsPage(QWidget):
    """Audio playback settings."""

    def __init__(self):
        super().__init__()
        self.settings = SettingsManager()
        self.setObjectName("audioSettingsPage")

        self.titleLabel = QLabel("Audio")
        self.titleLabel.setObjectName("settingsPageTitle")

        self.descriptionLabel = QLabel(
            "Configure audio playback and default audio behavior."
        )
        self.descriptionLabel.setObjectName("settingsPageDescription")
        self.descriptionLabel.setWordWrap(True)

        self.playbackFrame = QFrame()
        self.playbackFrame.setObjectName("audioSettingsSection")
        self.playbackTitle = QLabel("Playback")
        self.playbackTitle.setObjectName("settingsSectionTitle")

        self.autoPlayCheck = self._createCheckBox(
            "Automatically play media when opened", "audio/auto_play"
        )
        self.resumePlaybackCheck = self._createCheckBox(
            "Resume playback from the previous position", "audio/resume_playback"
        )
        self.rememberPositionCheck = self._createCheckBox(
            "Remember playback position", "audio/remember_position"
        )

        playbackLayout = QVBoxLayout(self.playbackFrame)
        playbackLayout.setContentsMargins(18, 16, 18, 16)
        playbackLayout.setSpacing(14)
        playbackLayout.addWidget(self.playbackTitle)
        playbackLayout.addWidget(self.autoPlayCheck)
        playbackLayout.addWidget(self.resumePlaybackCheck)
        playbackLayout.addWidget(self.rememberPositionCheck)

        self.volumeFrame = QFrame()
        self.volumeFrame.setObjectName("audioSettingsSection")
        self.volumeTitle = QLabel("Volume")
        self.volumeTitle.setObjectName("settingsSectionTitle")

        self.defaultVolumeLabel = QLabel()
        self.defaultVolumeLabel.setMinimumWidth(45)
        self.defaultVolumeLabel.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        self.defaultVolumeSlider = QSlider(Qt.Orientation.Horizontal)
        self.defaultVolumeSlider.setRange(0, 100)
        self.defaultVolumeSlider.valueChanged.connect(self._saveDefaultVolume)

        self.rememberVolumeCheck = self._createCheckBox(
            "Remember volume between sessions", "audio/remember_volume"
        )

        volumeRow = QHBoxLayout()
        volumeRow.setSpacing(12)
        volumeRow.addWidget(QLabel("Default Volume"))
        volumeRow.addWidget(self.defaultVolumeSlider, 1)
        volumeRow.addWidget(self.defaultVolumeLabel)

        volumeLayout = QVBoxLayout(self.volumeFrame)
        volumeLayout.setContentsMargins(18, 16, 18, 16)
        volumeLayout.setSpacing(14)
        volumeLayout.addWidget(self.volumeTitle)
        volumeLayout.addLayout(volumeRow)
        volumeLayout.addWidget(self.rememberVolumeCheck)

        self.modeFrame = QFrame()
        self.modeFrame.setObjectName("audioSettingsSection")
        self.modeTitle = QLabel("Playback Mode")
        self.modeTitle.setObjectName("settingsSectionTitle")

        self.loopCombo = QComboBox()
        self.loopCombo.addItem("Loop Off", 0)
        self.loopCombo.addItem("Loop Playlist", 1)
        self.loopCombo.addItem("Loop One", 2)
        self.loopCombo.currentIndexChanged.connect(self._saveLoopMode)

        self.shuffleCheck = self._createCheckBox(
            "Enable shuffle by default", "audio/default_shuffle"
        )

        modeForm = QFormLayout()
        modeForm.setHorizontalSpacing(20)
        modeForm.setVerticalSpacing(14)
        modeForm.addRow("Default Loop Mode", self.loopCombo)

        modeLayout = QVBoxLayout(self.modeFrame)
        modeLayout.setContentsMargins(18, 16, 18, 16)
        modeLayout.setSpacing(14)
        modeLayout.addWidget(self.modeTitle)
        modeLayout.addLayout(modeForm)
        modeLayout.addWidget(self.shuffleCheck)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)
        layout.addWidget(self.titleLabel)
        layout.addWidget(self.descriptionLabel)
        layout.addSpacing(6)
        layout.addWidget(self.playbackFrame)
        layout.addWidget(self.volumeFrame)
        layout.addWidget(self.modeFrame)
        layout.addStretch()

        self._loadSettings()

    def _createCheckBox(self, text, key):
        checkbox = QCheckBox(text)
        checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        checkbox.toggled.connect(
            lambda checked, k=key: self.settings.set(k, checked)
        )
        return checkbox

    @staticmethod
    def _toBool(value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in ("1", "true", "yes", "on")
        return bool(value)

    @staticmethod
    def _toInt(value, default=0):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _loadSettings(self):
        self.autoPlayCheck.setChecked(
            self._toBool(self.settings.get("audio/auto_play"))
        )
        self.resumePlaybackCheck.setChecked(
            self._toBool(self.settings.get("audio/resume_playback"))
        )
        self.rememberPositionCheck.setChecked(
            self._toBool(self.settings.get("audio/remember_position"))
        )

        volume = max(
            0,
            min(100, self._toInt(self.settings.get("audio/default_volume"), 100)),
        )
        self.defaultVolumeSlider.setValue(volume)
        self._updateVolumeLabel(volume)

        self.rememberVolumeCheck.setChecked(
            self._toBool(self.settings.get("audio/remember_volume"))
        )

        loop_mode = self._toInt(self.settings.get("audio/default_loop_mode"), 0)
        self.loopCombo.setCurrentIndex(max(0, min(2, loop_mode)))

        self.shuffleCheck.setChecked(
            self._toBool(self.settings.get("audio/default_shuffle"))
        )

    def _saveDefaultVolume(self, value):
        self._updateVolumeLabel(value)
        self.settings.set("audio/default_volume", value)

    def _saveLoopMode(self, index):
        self.settings.set("audio/default_loop_mode", index)

    def _updateVolumeLabel(self, value):
        self.defaultVolumeLabel.setText(f"{value}%")

    def applyTheme(self, colors):
        text = colors["text"]
        secondary = colors.get("secondary_text", text)
        border = colors["border"]
        media = colors["media"]
        hover = colors["button_hover"]

        self.setStyleSheet(f'''
            QWidget#audioSettingsPage {{
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
            QFrame#audioSettingsSection {{
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
            QCheckBox {{
                color: {text};
                font-size: 15px;
                spacing: 10px;
                background: transparent;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border: 2px solid {border};
                border-radius: 6px;
                background-color: {media};
            }}
            QCheckBox::indicator:hover {{
                border-color: #FF3344;
            }}
            QCheckBox::indicator:checked {{
                background-color: #FF3344;
                border-color: #FF3344;
            }}
            QSlider::groove:horizontal {{
                height: 6px;
                background-color: {hover};
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                width: 16px;
                margin: -5px 0;
                border-radius: 8px;
                background-color: #FF3344;
            }}
            QComboBox {{
                min-height: 36px;
                padding: 0 12px;
                color: {text};
                background-color: {media};
                border: 1px solid {border};
                border-radius: 8px;
            }}
            QComboBox:hover {{
                border-color: #FF3344;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 28px;
            }}
            QComboBox QAbstractItemView {{
                color: {text};
                background-color: {media};
                border: 1px solid {border};
                selection-background-color: #FF3344;
                selection-color: white;
            }}
        ''')
