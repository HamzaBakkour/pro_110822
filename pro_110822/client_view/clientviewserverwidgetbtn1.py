from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QFont

from PySide6.QtWidgets import QSizePolicy




class ClientViewServerWidgetBtn1(QtWidgets.QPushButton):
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self._width : int
        self._hight : int
        
        self._set_font_style()
        self._set_style()



    def _set_style(self):
        self.setStyleSheet(u"QPushButton::flat\n"
                                        "{\n"
                                        "       background-color: #8c8b8b;\n"
                                        "       border: 1px solid black;\n"
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

        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFlat(True)
        self.setCheckable(True)

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

