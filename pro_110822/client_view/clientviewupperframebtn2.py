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



class ClientViewUpperFrameBtn2(QtWidgets.QPushButton):
    def __init__(self, *args,**kwargs):
<<<<<<< HEAD
        super().__init__(*args, **kwargs)
=======
        super(ClientViewUpperFrameBtn2, self).__init__(*args, **kwargs)
>>>>>>> b04d7d4cc4a07e99918ac70c6b9d380a9e62ae72
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
                                        "       background-color: #0279f0;\n"
                                        "       border: 1px solid #0279f0;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton::pressed\n"
                                        "{\n"
                                        "       background-color: #2590fa;\n"
                                        "       border: 1px solid #2590fa;\n"
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

