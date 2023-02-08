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


class ClientViewUpperFrame(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs):
        super(ClientViewUpperFrame, self).__init__(*args, **kwargs)
        self.searchBtton : QtWidgets.QPushButton

        self._set_style()
        self._initUi()

    def _set_style(self):
        self.setStyleSheet(u"    background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 57, 57, 255),stop:1 rgba(50, 50, 50, 255));\n"
                            "    border: 1px solid #222;\n"
                            "    padding: 4px;\n"
                            "    color: #fff;")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)



    def _initUi(self):
        self.searchBtton = clientviewupperframebtn1.ClientViewUpperFrameBtn1(self)
        self.searchBtton.set_size(100, 199)
        self.searchBtton.set_text('Search for servers')
        # self.searchBtton.setText('Search for servers')
        # self.searchBtton.set_geometry(450, 70, 131, 131)



        # , 450, 70, 131, 131, 'Search for servers'


        # #Create a server button
        # self.createButton = QPushButton(self)
        # self.createButton.setObjectName(u"pushButton_2")
        # self.createButton.setGeometry(QRect(300, 70, 131, 31))
        # sizePolicy.setHeightForWidth(self.createButton.sizePolicy().hasHeightForWidth())
        # self.createButton.setSizePolicy(sizePolicy)
        # self.createButton.setFont(font)
        # self.createButton.setStyleSheet(u"QPushButton::flat\n"
        #                                 "{\n"
        #                                 "       background-color: transparent;\n"
        #                                 "       border: none;\n"
        #                                 "       color: #fff;\n"
        #                                 "}\n"
        #                                 "\n"
        #                                 "QPushButton::hover\n"
        #                                 "{\n"
        #                                 "       background-color: #0279f0;\n"
        #                                 "       border: 1px solid #0279f0;\n"
        #                                 "}\n"
        #                                 "\n"
        #                                 "QPushButton::pressed\n"
        #                                 "{\n"
        #                                 "       background-color: #2590fa;\n"
        #                                 "       border: 1px solid #2590fa;\n"
        #                                 "}\n"
        #                                 "")
        
        # self.searchButton.setText('Search for servers')
        # self.createButton.setText('Create a server')
        pass