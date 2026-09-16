from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QFrame, QLabel, QVBoxLayout, QWidget

from ..settings_manager import SettingsManager


class CoreSettingsPage(QWidget):
    """Core application behavior settings."""

    def __init__(self):
        super().__init__()
        self.settings = SettingsManager()
        self.setObjectName("coreSettingsPage")

        self.titleLabel = QLabel("Core")
        self.titleLabel.setObjectName("settingsPageTitle")

        self.descriptionLabel = QLabel(
            "Configure application startup, playlist, and exit behavior."
        )
        self.descriptionLabel.setObjectName("settingsPageDescription")
        self.descriptionLabel.setWordWrap(True)

        self.startupFrame = QFrame()
        self.startupFrame.setObjectName("coreSettingsSection")
        self.startupTitle = QLabel("Startup & Session")
        self.startupTitle.setObjectName("settingsSectionTitle")

        self.rememberLastMediaCheck = self._createCheckBox(
            "Remember last opened media", "core/remember_last_media"
        )
        self.rememberLastPlaylistCheck = self._createCheckBox(
            "Remember last playlist", "core/remember_last_playlist"
        )

        startupLayout = QVBoxLayout(self.startupFrame)
        startupLayout.setContentsMargins(18, 16, 18, 16)
        startupLayout.setSpacing(14)
        startupLayout.addWidget(self.startupTitle)
        startupLayout.addWidget(self.rememberLastMediaCheck)
        startupLayout.addWidget(self.rememberLastPlaylistCheck)

        self.applicationFrame = QFrame()
        self.applicationFrame.setObjectName("coreSettingsSection")
        self.applicationTitle = QLabel("Application Behavior")
        self.applicationTitle.setObjectName("settingsSectionTitle")

        self.addOpenedFilesCheck = self._createCheckBox(
            "Automatically add opened files to playlist",
            "core/add_opened_files_to_playlist",
        )
        self.confirmBeforeExitCheck = self._createCheckBox(
            "Confirm before exiting Pav Play", "core/confirm_before_exit"
        )

        applicationLayout = QVBoxLayout(self.applicationFrame)
        applicationLayout.setContentsMargins(18, 16, 18, 16)
        applicationLayout.setSpacing(14)
        applicationLayout.addWidget(self.applicationTitle)
        applicationLayout.addWidget(self.addOpenedFilesCheck)
        applicationLayout.addWidget(self.confirmBeforeExitCheck)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)
        layout.addWidget(self.titleLabel)
        layout.addWidget(self.descriptionLabel)
        layout.addSpacing(6)
        layout.addWidget(self.startupFrame)
        layout.addWidget(self.applicationFrame)
        layout.addStretch()

        self._loadSettings()

    def _createCheckBox(self, text, key):
        checkbox = QCheckBox(text)
        checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        checkbox.toggled.connect(lambda checked, k=key: self.settings.set(k, checked))
        return checkbox

    @staticmethod
    def _toBool(value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in ("1", "true", "yes", "on")
        return bool(value)

    def _loadSettings(self):
        self.rememberLastMediaCheck.setChecked(
            self._toBool(self.settings.get("core/remember_last_media"))
        )
        self.rememberLastPlaylistCheck.setChecked(
            self._toBool(self.settings.get("core/remember_last_playlist"))
        )
        self.addOpenedFilesCheck.setChecked(
            self._toBool(self.settings.get("core/add_opened_files_to_playlist"))
        )
        self.confirmBeforeExitCheck.setChecked(
            self._toBool(self.settings.get("core/confirm_before_exit"))
        )

    def applyTheme(self, colors):
        text = colors["text"]
        secondary = colors.get("secondary_text", text)
        border = colors["border"]
        media = colors["media"]

        self.setStyleSheet(f"""
            QWidget#coreSettingsPage {{
                background: transparent;
                border: none;
            }}
            QLabel#settingsPageTitle {{
                color: #FF3344;
                font-size: 28px;
                font-weight: 700;
                background: transparent;
            }}
            QLabel#settingsPageDescription {{
                color: {secondary};
                font-size: 14px;
                background: transparent;
            }}
            QFrame#coreSettingsSection {{
                background-color: {media};
                border: 1px solid {border};
                border-radius: 18px;
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
        """)
