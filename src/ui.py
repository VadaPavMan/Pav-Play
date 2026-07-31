from PySide6.QtGui import QIcon, QPixmap, QAction, QFont
from PySide6.QtCore import QSize, Qt, QCoreApplication, QMetaObject, QRect
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QHBoxLayout, 
    QMenu, QMenuBar, QSizePolicy, QSlider, QSpacerItem, QStatusBar, 
    QToolButton, QVBoxLayout, QWidget, QPushButton)    
import sys
import os

WIDTH = 1280
HEIGHT = 720

class MainUi(object):
    def setup(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(QSize(WIDTH, HEIGHT))
        
        # Setup central widget & layout
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.mainLayout = QVBoxLayout()
        self.centralwidget.setLayout(self.mainLayout)
        
        # Currently Playing 
        self.songLabel = QLabel(f"Now Playing: {"Lund Playing"}")
        self.songLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.songLabel)
        
        # create a label
        self.singerName = QLabel("I Don't Know May Be Someone...")
        self.singerName.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.singerName)
        
        # create a button
        self.playButton = QPushButton("Play")
        
        # create a button (pause)
        self.pauseButton = QPushButton("Pause")
        
        # create a next button
        self.nextButton = QPushButton("Next")
        
        # create a previous button
        self.previousButton = QPushButton("Previous")
        
        # create Horizontal Layout
        self.controlsLayout = QHBoxLayout()
        self.controlsLayout.addWidget(self.playButton)
        self.controlsLayout.addWidget(self.pauseButton)
        self.controlsLayout.addWidget(self.previousButton)
        self.controlsLayout.addWidget(self.nextButton)
        self.mainLayout.addLayout(self.controlsLayout)
        
        # # 3. Setup image label
        # self.image_label = QLabel()
        # basedir = os.path.dirname(__file__)
        
        # # 4. FIX: Safely join paths across all operating systems
        # parent_dir = os.path.dirname(basedir)
        # self.image_path = os.path.join(parent_dir, "assets", "relaxation.png")
        
        # # --- DEBUGGING CHECKS ---
        # # These will print to your terminal/console when you run the app
        # print(f"Looking for image at: {self.image_path}")
        # print(f"Does the file exist? {os.path.exists(self.image_path)}")
        # # ------------------------

        # self.pixmap = QPixmap(self.image_path)
        
        # if self.pixmap.isNull():
        #     print("ERROR: Pixmap loaded empty. The image file is missing or corrupted.")
        
        # self.image_label.setPixmap(self.pixmap)
        # self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # # Add label to our safely named layout
        # self.verticalLayout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
    def addLabel(self, Text):
        label = QLabel(Text)
        label.setAlignment(Qt.AlignCenter)
        return label