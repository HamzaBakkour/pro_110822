import sys
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QApplication, QFormLayout, QScrollArea, QGridLayout, QPushButton
import networkScanner
from deviceWidget import device

class scrollPanel(QScrollArea):

    def __init__(self, parent= None):
        super().__init__()
        self.initUI()
    
    def initUI(self):

        self.scroll_panel = QtWidgets.QWidget()
        self.scroll_panel_layout = QFormLayout(self.scroll_panel)
        self.scroll_panel_layout.setContentsMargins(0,0,0,0)

        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidget(self.scroll_panel)

        available = networkScanner.get_connected_devices_name()
 

        for element in available:
            available_device = device(element[0], element[2])
            self.scroll_panel_layout.addWidget(available_device)

