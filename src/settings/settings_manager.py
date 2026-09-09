"""Persistent settings storage for Pav Play."""

from PySide6.QtCore import QSettings

from .settings_defaults import DEFAULT_SETTINGS


class SettingsManager:
    """Small wrapper around QSettings used by the Settings UI."""

    def __init__(self):
        self.settings = QSettings("Pav Play", "Pav Play")

    def get(self, key):
        default = DEFAULT_SETTINGS.get(key)
        return self.settings.value(key, defaultValue=default)

    def set(self, key, value):
        self.settings.setValue(key, value)
        self.settings.sync()

    def reset(self, key):
        if key in DEFAULT_SETTINGS:
            self.set(key, DEFAULT_SETTINGS[key])
        else:
            self.settings.remove(key)

    def reset_all(self):
        self.settings.clear()
        self.settings.sync()
