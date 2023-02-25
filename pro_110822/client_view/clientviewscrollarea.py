import sys
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QApplication, QFormLayout, QScrollArea, QGridLayout, QPushButton


class ClientViewScrollArea(QScrollArea):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()
    
    def init_ui(self):
        self.scrollPanel = QtWidgets.QWidget()
        self.scrollPanelLayout = QFormLayout(self.scrollPanel)
        self.scrollPanelLayout.setHorizontalSpacing(0)
        self.scrollPanelLayout.setAlignment(QtCore.Qt.AlignTop)
        self.scrollPanelLayout.setContentsMargins(0,7,0,0)

        self.setWidgetResizable(True)
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidget(self.scrollPanel)

    def add_device(self, device: QtWidgets.QWidget):
        self.scrollPanelLayout.addWidget(device)
    
    def reseat(self):
        for i in reversed(range(self.scrollPanelLayout.count())): 
            self.scrollPanelLayout.itemAt(i).widget().deleteLater()
        pass

