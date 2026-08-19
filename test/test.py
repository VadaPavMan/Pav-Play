import sys
import os
import random
from PyQt6.QtCore import Qt, QUrl, QTime, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QAction, QKeyEvent, QDragEnterEvent, QDropEvent, QColor, QPalette
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QListWidget, QListWidgetItem, QSplitter,
                             QPushButton, QSlider, QLabel, QFileDialog, QMessageBox,
                             QStatusBar, QToolBar, QStackedWidget, QSizePolicy,
                             QMenu, QFrame, QToolTip)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

