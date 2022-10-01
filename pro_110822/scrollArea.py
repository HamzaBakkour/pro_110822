import sys
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QApplication, QFormLayout, QScrollArea, QGridLayout, QPushButton
# import networkScanner
from devicewidget import Device

class ScrollPanel(QScrollArea):

    def __init__(self, parent= None):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.scroll_panel = QtWidgets.QWidget()
        self.scroll_panel_layout = QFormLayout(self.scroll_panel)

        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidget(self.scroll_panel)

    def addDevice(self, device: QtWidgets.QWidget):
        self.scroll_panel_layout.addWidget(device)
    
    def reseat(self):
        for i in reversed(range(self.scroll_panel_layout.count())): 
            self.scroll_panel_layout.itemAt(i).widget().deleteLater()
        pass

