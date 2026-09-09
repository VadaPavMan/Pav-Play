from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QIcon

from .pages import (
    AudioSettingsPage,
    VideoSettingsPage,
    CoreSettingsPage,
    HelpPage,
    AboutPage,
)

from icons import Icons


class SettingsPage(QWidget):
    """Settings shell: sidebar navigation + content stack."""

    backRequested = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("settingsPage")

        self.sidebarFrame = QFrame()
        self.sidebarFrame.setObjectName("settingsSidebar")
        self.sidebarFrame.setFixedWidth(210)

        self.contentFrame = QFrame()
        self.contentFrame.setObjectName("settingsContent")

        sidebarLayout = QVBoxLayout(self.sidebarFrame)
        sidebarLayout.setContentsMargins(14, 14, 14, 14)
        sidebarLayout.setSpacing(10)

        self.backButton = self._makeButton(
            " Back", icon_path=Icons.BACK, checkable=False
        )
        self.backButton.clicked.connect(self.backRequested.emit)
        sidebarLayout.addWidget(self.backButton)
        sidebarLayout.addSpacing(8)

        self.categoryButtons = []
        self.audioButton = self._makeButton("Audio")
        self.videoButton = self._makeButton("Video")
        self.coreButton = self._makeButton("Core")
        self.helpButton = self._makeButton("Help")
        self.aboutButton = self._makeButton("About")

        self.categoryButtons.extend(
            [
                self.audioButton,
                self.videoButton,
                self.coreButton,
                self.helpButton,
                self.aboutButton,
            ]
        )

        for button in self.categoryButtons:
            sidebarLayout.addWidget(button)

        sidebarLayout.addStretch()

        self.contentStack = QStackedWidget()
        self.contentStack.setObjectName("settingsContentStack")
        contentLayout = QVBoxLayout(self.contentFrame)
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.addWidget(self.contentStack)

        self.pages = [
            AudioSettingsPage(),
            VideoSettingsPage(),
            CoreSettingsPage(),
            HelpPage(),
            AboutPage(),
        ]

        for page in self.pages:
            self.contentStack.addWidget(page)

        for index, button in enumerate(self.categoryButtons):
            button.clicked.connect(lambda checked=False, i=index: self.showPage(i))

        self.contentStack.setCurrentIndex(0)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.addWidget(self.sidebarFrame)
        layout.addWidget(self.contentFrame, 1)

        self._activeIndex = 0

    def _makeButton(self, text, icon_path=None, checkable=True):
        button = QPushButton(text)
        if icon_path:
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(48, 48))
            button.setFlat(True)
            button.setStyleSheet("border: none; background: transparent;")
        else:
            button.setIcon(QIcon())
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setMinimumHeight(58)
        button.setCheckable(checkable)
        return button

    def showPage(self, index):
        self._activeIndex = index
        self.contentStack.setCurrentIndex(index)
        for i, button in enumerate(self.categoryButtons):
            button.setChecked(i == index)

    def applyTheme(self, colors):
        self.setStyleSheet(
            "QWidget#settingsPage { background: transparent; border: none; }"
        )

        self.sidebarFrame.setStyleSheet(f"""
            QFrame#settingsSidebar {{
                background-color: {colors['nav']};
                border: 1px solid {colors['border']};
                border-radius: 12px;
            }}
        """)

        self.contentFrame.setStyleSheet(f"""
            QFrame#settingsContent {{
                background-color: {colors['media']};
                border: 1px solid {colors['border']};
                border-radius: 12px;
            }}
        """)

        self.contentStack.setStyleSheet(
            "QStackedWidget#settingsContentStack { background: transparent; border: none; }"
        )

        normal = colors["text"]
        hover = colors["button_hover"]
        selected_bg = "rgba(255, 51, 68, 35)"

        for button in self.categoryButtons:
            button.setStyleSheet(f"""
                QPushButton {{
                    color: black;
                    background: "#ecebe4";
                    border: 2px solid black;
                    border-radius: 18px;
                    font-size: 17px;
                    font-weight: 600;
                    text-align: left;
                    padding: 0px 16px;
                }}
                QPushButton:hover {{
                    color: #FF3344;
                    background-color: #121212;
                    border-color: #FF3344;
                }}
                QPushButton:checked {{
                    color: #FF3344;
                    background-color: #121212;
                    border-color: #FF3344;
                }}
            """)

        self.backButton.setStyleSheet(f"""
            QPushButton {{
                color: black;
                background: "#ecebe4";
                border: 2px solid black;
                border-radius: 18px;
                font-size: 17px;
                font-weight: 600;
                text-align: left;
                padding: 0px 16px;
            }}
            QPushButton:hover {{
                color: #FF3344;
                background-color: "#121212";
                border-color: #FF3344;
            }}
        """)

        for page in self.pages:
            page.applyTheme(colors)
