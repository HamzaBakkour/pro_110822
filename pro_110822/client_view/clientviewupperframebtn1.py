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

class ClientViewUpperFrameBtn1(QtWidgets.QPushButton):
    def __init__(self, *args,**kwargs):
        super(ClientViewUpperFrameBtn1, self).__init__(*args, **kwargs)
        self._width : int
        self._hight : int
        
        self._set_style()
        self._set_font_style()


    def _set_style(self):
        self.setStyleSheet(u"QPushButton::flat\n"
                            "{\n"
                            "       background-color: transparent;\n"
                            "       border: none;\n"
                            "       color: #fff;\n"
                            "}\n"
                            "\n"
                            "QPushButton::hover\n"
                            "{\n"
                            "       background-color: #04c91b;\n"
                            "       border: 1px solid #04c91b;\n"
                            "}\n"
                            "\n"
                            "QPushButton::pressed\n"
                            "{\n"
                            "       background-color: #02f01e;\n"
                            "       border: 1px solid #02f01e;\n"
                            "}\n"
                            "")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFlat(False)


    def _set_font_style(self):
        font = QFont()
        font.setBold(True)
        self.setFont(font)

    def set_size(self, w, h):
        self._width = w
        self._hight = h

    def set_text(self, text):
        self.setText(text)

    def sizeHint(self):
        try:
            return QtCore.QSize(self._width, self._hight)
        except AttributeError:
            return QtCore.QSize()



    # def __init__(self, *args, width, hight, **kwargs):
    #     super(ClientViewUpperFrameBtn1, self).__init__(*args, width, hight, **kwargs)