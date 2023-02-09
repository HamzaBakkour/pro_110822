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
from . import clientviewupperframebtn1
from . import clientviewupperframebtn2

class ClientViewUpperFrame(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs):
        super(ClientViewUpperFrame, self).__init__(*args, **kwargs)

        self.layout = QGridLayout(self)
        self.searchBtton : QtWidgets.QPushButton
        self.createBtton : QtWidgets.QPushButton
        
        self._set_style()
        self._init_ui()

    def _set_style(self):
        self.setStyleSheet(u"    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 57, 57, 255),stop:1 rgba(50, 50, 50, 255));\n"
                            "    border: 1px solid #222;\n"
                            "    padding: 4px;\n"
                            "    color: #fff;")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)



    def _init_ui(self):

        self.searchBtton = clientviewupperframebtn1.ClientViewUpperFrameBtn1()
        self.searchBtton.set_text('Search for servers')

        self.createBtton = clientviewupperframebtn2.ClientViewUpperFrameBtn2()
        self.createBtton.set_text('Create a server')

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 1)
        self.layout.setRowStretch(2, 1)

        searchCreateButtonLayout = QGridLayout()
        searchCreateButtonLayout.setContentsMargins(0, 0, 0, 0)
        searchCreateButtonLayout.setSpacing(0)
        searchCreateButtonLayout.setColumnStretch(0, 12)
        searchCreateButtonLayout.setColumnStretch(1, 1)
        searchCreateButtonLayout.setColumnStretch(2, 12)
        searchCreateButtonLayout.setColumnStretch(3, 1)

        searchCreateButtonLayout.addWidget(self.searchBtton, 0, 0)
        searchCreateButtonLayout.addWidget(self.createBtton, 0, 2)

        self.layout.addLayout(searchCreateButtonLayout, 2,1)