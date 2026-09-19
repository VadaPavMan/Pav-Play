from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from src.icons import Icons


class HelpPage(QWidget):

    GITHUB_ISSUES_URL = "https://github.com/VadaPavMan/Pav-Play/issues"
    DEVELOPER_EMAIL = "harshrajbhar071@gmail.com"

    def __init__(self):
        super().__init__()
        self.setObjectName("helpPage")

        self._sections = []

        self._buildUi()

    def _buildUi(self):
        outerLayout = QVBoxLayout(self)
        outerLayout.setContentsMargins(20, 20, 20, 20)
        outerLayout.setSpacing(14)

        title = QLabel("Help")
        title.setObjectName("helpTitle")
        outerLayout.addWidget(title)

        subtitle = QLabel(
            "Learn how to use Pav Play and find out how to report bugs or problems."
        )
        subtitle.setObjectName("helpSubtitle")
        subtitle.setWordWrap(True)
        outerLayout.addWidget(subtitle)

        scrollArea = QScrollArea()
        scrollArea.setObjectName("helpScrollArea")
        scrollArea.setWidgetResizable(True)
        scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        scrollArea.viewport().setStyleSheet("background: transparent; border: none;")

        content = QWidget()
        contentLayout = QVBoxLayout(content)
        contentLayout.setContentsMargins(10, 10, 10, 10)
        contentLayout.setSpacing(12)
        content.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.howToUseSection = self._createExpandableSection(
            "How To Use Pav Play",
            self._buildHowToUseContent(),
        )
        contentLayout.addWidget(self.howToUseSection)

        self.reportBugSection = self._createExpandableSection(
            "How To Report A Bug",
            self._buildBugReportContent(),
        )
        contentLayout.addWidget(self.reportBugSection)

        contentLayout.addStretch()
        scrollArea.setWidget(content)
        outerLayout.addWidget(scrollArea, 1)

        # Start with the main usage guide expanded.
        self._setSectionExpanded(self.howToUseSection, True)

    def _createExpandableSection(self, titleText, contentWidget):
        section = QFrame()
        section.setObjectName("helpSection")

        sectionLayout = QVBoxLayout(section)
        sectionLayout.setContentsMargins(0, 0, 0, 0)
        sectionLayout.setSpacing(0)

        headerButton = QToolButton()
        headerButton.setObjectName("helpSectionHeader")
        headerButton.setText(titleText)
        headerButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        headerButton.setArrowType(Qt.ArrowType.RightArrow)
        headerButton.setCursor(Qt.CursorShape.PointingHandCursor)
        headerButton.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        headerButton.setMinimumHeight(52)

        contentFrame = QFrame()
        contentFrame.setObjectName("helpSectionContent")
        contentFrame.setVisible(False)

        contentLayout = QVBoxLayout(contentFrame)
        contentLayout.setContentsMargins(18, 16, 18, 18)
        contentLayout.setSpacing(12)
        contentLayout.addWidget(contentWidget)

        sectionLayout.addWidget(headerButton)
        sectionLayout.addWidget(contentFrame)

        section._headerButton = headerButton
        section._contentFrame = contentFrame

        headerButton.clicked.connect(
            lambda checked=False, s=section: self._toggleSection(s)
        )

        self._sections.append(section)
        return section

    def _toggleSection(self, section):
        expanded = not section._contentFrame.isVisible()
        self._setSectionExpanded(section, expanded)

    def _setSectionExpanded(self, section, expanded):
        section._contentFrame.setVisible(expanded)

        section._headerButton.setArrowType(
            Qt.ArrowType.DownArrow if expanded else Qt.ArrowType.RightArrow
        )

    def _buildHowToUseContent(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self._addGuideBlock(
            layout,
            "1. Open Media",
            "Use the Files button in the top navigation to select supported "
            "audio or video files. You can also use the Folder option or "
            "drag and drop media into Pav Play.",
        )

        self._addGuideBlock(
            layout,
            "2. Playlist",
            "Opened media can appear in the playlist. Select a playlist item "
            "to play it, double-click an item to start playback, or use the "
            "playlist context menu for actions such as Play, Remove, and "
            "Clear Playlist.",
        )

        self._addGuideBlock(
            layout,
            "3. Player",
            "The main player area switches between the video player and the "
            "music player depending on the selected media type.",
        )

        self._addGuideBlock(
            layout,
            "4. Playback Controls",
            "Use Play/Pause, Previous, Next, Shuffle, Loop, and Volume controls "
            "from the control bar. The position slider lets you seek through "
            "the current media.",
        )

        self._addGuideBlock(
            layout,
            "5. Supported Media",
            "Pav Play supports the audio and video formats defined by the "
            "application's central media-format configuration.",
        )

        self._addGuideBlock(
            layout,
            "6. Theme",
            "Use the theme button in the top navigation to switch between "
            "Light and Dark themes.",
        )

        self._addGuideBlock(
            layout,
            "7. Settings",
            "Open Settings to configure Audio, Video, and Core behavior. "
            "Help and About are also available from the Settings sidebar.",
        )

        self._addGuideBlock(
            layout,
            "8. Important Playback Settings",
            "Audio and Video settings can control Auto Play and Resume Playback. "
            "Core settings control application behavior such as remembering "
            "the last media, remembering the playlist, exit confirmation, "
            "and automatically adding opened files to the playlist.",
        )

        return widget

    def _addGuideBlock(self, layout, heading, body):
        headingLabel = QLabel(heading)
        headingLabel.setObjectName("helpBlockHeading")

        bodyLabel = QLabel(body)
        bodyLabel.setObjectName("helpBlockBody")
        bodyLabel.setWordWrap(True)
        bodyLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        layout.addWidget(headingLabel)
        layout.addWidget(bodyLabel)

    def _buildBugReportContent(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        intro = QLabel(
            "Before reporting a bug, gather enough information for the "
            "developer to reproduce and investigate the problem."
        )
        intro.setObjectName("helpBlockBody")
        intro.setWordWrap(True)
        layout.addWidget(intro)

        self._addGuideBlock(
            layout,
            "What to include",
            "Describe what you were doing, what you expected to happen, "
            "what actually happened, and the steps required to reproduce it. "
            "Also include useful error messages, screenshots, the media format "
            "involved, and any other relevant details.",
        )

        self._addGuideBlock(
            layout,
            "Where to report",
            "You can report the issue through the Pav Play GitHub Issues page "
            "or contact the developer by email.",
        )

        githubButton = self._createLinkButton(
            "Report on GitHub",
            Icons.GITHUB,
            self.GITHUB_ISSUES_URL,
        )
        githubButton.setStyleSheet(self.setButtonStyle())
        layout.addWidget(githubButton)

        self.emailButton = self._createLinkButton(
            "Email the Developer",
            Icons.EMAIL,
            "mailto:" + self.DEVELOPER_EMAIL,
        )
        self.emailButton.setStyleSheet(self.setButtonStyle())
        self.emailButton.clicked.connect(self.openEmail)
        layout.addWidget(self.emailButton)

        contactInfo = QLabel(f"Developer email: {self.DEVELOPER_EMAIL}")
        contactInfo.setObjectName("helpContactInfo")
        contactInfo.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        layout.addWidget(contactInfo)

        return widget

    def setButtonStyle(self):
        return """
            QPushButton#helpLinkButton{
                color: black;
                background-color: "#ecebe4";
                border: 2px solid black;
                border-radius: 18px;
                font-size: 14px;
                font-weight: bold;
                text-align: left;
                padding: 8px 14px;
            }
            
            QPushButton#helpLinkButton:hover {
                color: #FF3344;
                background-color: "#121212";
                border-color: #FF3344;
            }
        """

    def openEmail(self):
        QDesktopServices.openUrl(
            QUrl(
                f"https://mail.google.com/mail/?view=cm&fs=1&to={self.DEVELOPER_EMAIL}"
            )
        )

    def _createLinkButton(self, text, iconPath, url):
        button = QPushButton(text)
        button.setObjectName("helpLinkButton")
        button.setIcon(QIcon(iconPath))
        button.setIconSize(QSize(28, 28))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setMinimumHeight(48)
        button.clicked.connect(lambda checked=False, target=url: self._openUrl(target))
        return button

    def _openUrl(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def applyTheme(self, colors):
        self.setStyleSheet(f"""
            QWidget#helpPage {{
                background: transparent;
                border: none;
            }}

            QLabel#helpTitle {{
                color: #FF3344;
                background: transparent;
                font-size: 26px;
                font-weight: 700;
            }}

            QLabel#helpSubtitle {{
                color: {colors["text"]};
                background: transparent;
                font-size: 14px;
            }}

            QScrollArea#helpScrollArea {{
                background: transparent;
                border: none;
            }}

            QFrame#helpSection {{
                background-color: {colors["surface"]};
                border: 1px solid {colors["border"]};
                border-radius: 18px;
            }}

            QToolButton#helpSectionHeader {{
                color: {colors["text"]};
                background: transparent;
                border: none;
                border-radius: 18px;
                padding: 0px 14px;
                font-size: 16px;
                font-weight: bold;
                text-align: left;
            }}

            QToolButton#helpSectionHeader:hover {{
                color: #FF3344;
                background-color: {colors["button_hover"]};
            }}

            QFrame#helpSectionContent {{
                background: transparent;
                border: none;
                border-top: 1px solid black;
                margin: 20px;
            }}

            QLabel#helpBlockHeading {{
                color: #FF3344;
                background: transparent;
                font-size: 14px;
                font-weight: 700;
            }}

            QLabel#helpBlockBody {{
                color: {colors["text"]};
                background: transparent;
                font-size: 13px;
                line-height: 1.4;
            }}

            QLabel#helpContactInfo {{
                color: {colors["text"]};
                background: transparent;
                font-weight: bold;
                font-size: 13px;
            }}
            """)
