from PySide6 import QtCore, QtWidgets

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QScrollArea,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel
)

from . import serverviewupperframe
from . import serverviewscrollarea
from . import serverviewbottomframe


class ServerView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)

        self.upperFrame = serverviewupperframe.ServerViewUpperFrame()
        self.scrollArea = serverviewscrollarea.ServerViewScrollArea()
        self.bottomFrame = serverviewbottomframe.ServerViewBottomFrame()
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(0)

        self.layout.setRowStretch(0,5)
        self.layout.setRowStretch(1,30)
        self.layout.setRowStretch(2,1)

        self.layout.addWidget(self.upperFrame, 0, 0)
        self.layout.addWidget(self.scrollArea, 1, 0)
        self.layout.addWidget(self.bottomFrame, 2, 0)
        # self.scrollArea.add_device(serverwidget.ServerWidget('QT-TEST1-1001_PRO110822', ('255.255.255.255')))
        # self.scrollArea.add_device(serverwidget.ServerWidget('QT-TEST2-1001_PRO110822', ('255.255.255.255')))
        # self.scrollArea.add_device(serverwidget.ServerWidget('QT-TEST3-1001_PRO110822', ('255.255.255.255')))
        # self.scrollArea.add_device(serverwidget_old.ServerWidget('QT-TEST1-1001_PRO110822', ('255.255.255.255')))
        # self.scrollArea.add_device(serverwidget_old.ServerWidget('QT-TEST2-1001_PRO110822', ('255.255.255.255')))
