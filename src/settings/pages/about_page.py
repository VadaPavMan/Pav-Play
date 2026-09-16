from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from icons import Icons


class AboutPage(QWidget):

    DEVELOPER_GITHUB_URL = "https://github.com/VadaPavMan"

    def __init__(self):
        super().__init__()
        self.setObjectName("aboutPage")
        self._sections = []
        self._buildUi()

    def _buildUi(self):
        outerLayout = QVBoxLayout(self)
        outerLayout.setContentsMargins(20, 20, 20, 20)
        outerLayout.setSpacing(14)

        title = QLabel("About")
        title.setObjectName("aboutTitle")
        outerLayout.addWidget(title)

        description = QLabel(
            "Pav Play is a simple desktop multimedia player for playing audio "
            "and video files locally.\n"
            "It is open source and released under the MIT License."
        )
        description.setObjectName("aboutDescription")
        description.setWordWrap(True)
        outerLayout.addWidget(description)

        scrollArea = QScrollArea()
        scrollArea.setObjectName("aboutScrollArea")
        scrollArea.setWidgetResizable(True)
        scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        scrollArea.viewport().setAutoFillBackground(False)

        content = QWidget()
        content.setObjectName("aboutContent")
        content.setAutoFillBackground(False)
        content.setStyleSheet("background: transparent; border: none;")

        contentLayout = QVBoxLayout(content)
        contentLayout.setContentsMargins(10, 10, 10, 10)
        contentLayout.setSpacing(18)

        licenseSection = self._createExpandableSection(
            "MIT License",
            self._buildLicenseContent(),
        )
        contentLayout.addWidget(licenseSection)

        contentLayout.addWidget(self._buildCreditsSection())
        contentLayout.addWidget(self._buildDeveloperSection())
        contentLayout.addStretch()

        scrollArea.setWidget(content)
        outerLayout.addWidget(scrollArea, 1)

        self._setSectionExpanded(licenseSection, False)

    def _createExpandableSection(self, titleText, contentWidget):
        section = QFrame()
        section.setObjectName("aboutLicenseSection")

        sectionLayout = QVBoxLayout(section)
        sectionLayout.setContentsMargins(0, 0, 0, 0)
        sectionLayout.setSpacing(0)

        headerButton = QToolButton()
        headerButton.setObjectName("aboutSectionHeader")
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
        contentFrame.setObjectName("aboutSectionContent")
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

    def _buildLicenseContent(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        licenseLabel = QLabel(LICENSE_TEXT)
        licenseLabel.setObjectName("aboutLicenseText")
        licenseLabel.setWordWrap(True)
        licenseLabel.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        layout.addWidget(licenseLabel)

        return widget

    def _buildCreditsSection(self):
        section = QFrame()
        section.setObjectName("aboutStaticSection")

        layout = QVBoxLayout(section)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(12)

        heading = QLabel("Credits")
        heading.setObjectName("aboutSectionTitle")
        layout.addWidget(heading)

        intro = QLabel(
            "Pav Play icons, graphics, and design resources credits goes to "
            "following creators:"
        )
        intro.setObjectName("aboutBody")
        intro.setWordWrap(True)
        layout.addWidget(intro)

        self._addCredit(
            layout,
            " App Icon",
            "Xnimrodx",
            Icons.XNIMRODX,
            "https://www.flaticon.com/kr/authors/xnimrodx",
        )
        self._addCredit(
            layout,
            " Buttons Icon",
            "Muhammad Ali",
            Icons.MUHAMMADALI,
            "https://www.flaticon.com/authors/muhammad-ali",
        )
        self._addCredit(
            layout,
            " Dashboard Hero Icon",
            "Eucalyp",
            Icons.EUCALYP,
            "https://www.flaticon.com/authors/eucalyp",
        )
        self._addCredit(
            layout,
            " Audio Page Design Inspiration",
            "Miti Abulaiti",
            Icons.MITIABULAITI,
            "https://www.figma.com/@miti",
        )
        self._addCredit(
            layout,
            " Audio Page Hero Graphic",
            "Storyset",
            Icons.STORYSET,
            "https://www.magnific.com/es/autor/stories",
        )

        return section

    def _addCredit(self, layout, resourceName, creatorName, iconPath, url):
        button = QPushButton(f"{resourceName} — {creatorName}")
        button.setObjectName("aboutCreditButton")
        button.setIcon(QIcon(iconPath))
        button.setIconSize(QSize(34, 34))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setMinimumHeight(52)
        button.clicked.connect(lambda checked=False, target=url: self._openUrl(target))
        button.setStyleSheet(self.setButtonStyle())
        layout.addWidget(button)

    def _buildDeveloperSection(self):
        section = QFrame()
        section.setObjectName("aboutStaticSection")

        layout = QVBoxLayout(section)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(12)

        heading = QLabel("About Me")
        heading.setObjectName("aboutSectionTitle")
        layout.addWidget(heading)

        description = QLabel("Pav Play is developed and maintained by Harsh Rajbhar.")
        description.setObjectName("aboutBody")
        description.setWordWrap(True)
        layout.addWidget(description)

        githubButton = QPushButton("@VadaPavMan  —  Harsh Rajbhar")
        githubButton.setObjectName("aboutDeveloperButton")
        githubButton.setIcon(QIcon(Icons.VADAPAVMAN))
        githubButton.setIconSize(QSize(30, 30))
        githubButton.setCursor(Qt.CursorShape.PointingHandCursor)
        githubButton.setMinimumHeight(52)
        githubButton.clicked.connect(
            lambda checked=False: self._openUrl(self.DEVELOPER_GITHUB_URL)
        )
        githubButton.setStyleSheet(self.setButtonStyle())
        layout.addWidget(githubButton)

        return section

    def _openUrl(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def setButtonStyle(self):
        return """
        QPushButton#aboutCreditButton,
        QPushButton#aboutDeveloperButton {
            color: black;
            background-color: #ecebe4;
            border: 2px solid black;
            border-radius: 18px;
            font-size: 14px;
            font-weight: bold;
            text-align: left;
            padding: 8px 14px;
        }
        
        QPushButton#aboutCreditButton:hover,
        QPushButton#aboutDeveloperButton:hover {
            color: #FF3344;
            background-color: #121212;
            border-color: #FF3344;
        }
        """

    def applyTheme(self, colors):
        self.setStyleSheet(f"""
            QWidget#aboutPage {{
                background: transparent;
                border: none;
            }}

            QLabel#aboutTitle {{
                color: #FF3344;
                background: transparent;
                font-size: 26px;
                font-weight: 700;
            }}

            QLabel#aboutDescription {{
                color: {colors["text"]};
                background: transparent;
                font-size: 14px;
            }}

            QScrollArea#aboutScrollArea {{
                background: transparent;
                border: none;
            }}

            QFrame#aboutLicenseSection,
            QFrame#aboutStaticSection {{
                background-color: {colors["surface"]};
                border: 1px solid {colors["border"]};
                border-radius: 18px;
            }}

            QToolButton#aboutSectionHeader {{
                color: {colors["text"]};
                background: transparent;
                border: none;
                border-radius: 18px;
                padding: 0px 14px;
                font-size: 16px;
                font-weight: bold;
                text-align: left;
            }}

            QToolButton#aboutSectionHeader:hover {{
                color: #FF3344;
                background-color: {colors["button_hover"]};
            }}

            QFrame#aboutSectionContent {{
                background: transparent;
                border: none;
                border-top: 1px solid black;
                margin: 20px;
            }}

            QLabel#aboutSectionTitle {{
                color: #FF3344;
                background: transparent;
                font-size: 18px;
                font-weight: 700;
            }}

            QLabel#aboutBody,
            QLabel#aboutLicenseText {{
                color: {colors["text"]};
                background: transparent;
                font-size: 13px;
                line-height: 1.4;
            }}

            QPushButton#aboutCreditButton,
            QPushButton#aboutDeveloperButton {{
                color: black;
                background-color: "#ecebe4";
                border: 2px solid black;
                border-radius: 18px;
                font-size: 14px;
                font-weight: bold;
                text-align: left;
                padding: 8px 14px;
            }}

            QPushButton#aboutCreditButton:hover,
            QPushButton#aboutDeveloperButton:hover {{
                color: #FF3344;
                background-color: "#121212";
                border-color: #FF3344;
            }}
        """)


LICENSE_TEXT = 'MIT License\n\nCopyright (c) 2026 Harsh Rajbhar\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n'
