import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices


class Link:

    GITHUB_REPO = "https://github.com/VadaPavMan/Pav-Play"

    @staticmethod
    def direct(url: str):
        QDesktopServices.openUrl(QUrl(url))
