#pro_110822/firstOpenView.py

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
from . import clientviewbuttomframeprogressbar
#  import ClientViewButtomFrameBrogressBar

class ClientViewButtomFrame(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs):
        super(ClientViewButtomFrame, self).__init__(*args, **kwargs)

        self.layout = QGridLayout(self)
        self.brogressBar : QtWidgets.QProgressBar
        
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
        self.brogressBar = clientviewbuttomframeprogressbar.ClientViewButtomFrameBrogressBar()
        self.brogressBar.setValue(25)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setVerticalSpacing(0)
        self.layout.setHorizontalSpacing(0)
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,2)
        self.layout.setColumnStretch(2,1)

        self.layout.addWidget(self.brogressBar,0,0)


