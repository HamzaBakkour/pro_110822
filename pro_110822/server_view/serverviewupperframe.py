from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QRect
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QScrollArea,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QWidget,
    QFrame,
    QSizePolicy
)

from client_view import clientviewupperframe
from . import serverviewupperframebtn1


class ServerViewUpperFrame(clientviewupperframe.ClientViewUpperFrame):

    def _init_ui(self):
        self.stopButton = serverviewupperframebtn1.ServerViewUpperFrameBtn1()
        self.stopButton.set_text('Stop server')

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)
        self.layout.setColumnStretch(2, 1)

        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 1)
        self.layout.addWidget(self.stopButton, 1, 1)