from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class HelpPage(QWidget):
    def __init__(self):
        super().__init__()
        self.title = QLabel("Help")
        self.description = QLabel("Help and troubleshooting content will be added here.")
        self.description.setWordWrap(True)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(10)
        layout.addWidget(self.title)
        layout.addWidget(self.description)
        layout.addStretch()

    def applyTheme(self, colors):
        self.title.setStyleSheet("color: #FF3344; background: transparent; font-size: 24px; font-weight: 700;")
        self.description.setStyleSheet(f"color: {colors['text']}; background: transparent; font-size: 14px;")
