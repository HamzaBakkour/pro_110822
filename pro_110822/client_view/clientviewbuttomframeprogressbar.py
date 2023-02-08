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
    QSizePolicy,
    QProgressBar
)


class ClientViewButtomFrameBrogressBar(QtWidgets.QProgressBar):
    def __init__(self, *args, **kwargs):
        super(ClientViewButtomFrameBrogressBar, self).__init__(*args, **kwargs)
        self.setGeometry(0,0,20,30)
        # self.setGeometry(10, 10, 10, 10)
        # self.adjustSize()
        # self._set_style()


    def _set_style(self):
        # self.setStyleSheet(u"    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 57, 57, 255),stop:1 rgba(50, 50, 50, 255));\n"
        #                     "    border: 1px solid #222;\n"
        #                     "    padding: 1px;")

        self.setValue(0)
        self.setTextVisible(False)

    def value(self, value: int)-> None:
        self.setValue(value)

    def message(self, text: str)-> None:
        self.setText(text)
        self.adjustSize()

    def reseat(self):
        self.setValue(0)
        self.setText(' ')
   
    def sizeHint(self):
        return QtCore.QSize(10, 5)