import sys
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QApplication, QFormLayout, QScrollArea, QGridLayout, QPushButton
# import networkScanner

class ClientViewScrollArea(QScrollArea):

    def __init__(self, *args, **kwargs):
        super(ClientViewScrollArea, self).__init__(*args, **kwargs)
        self._set_style()
        self._init_ui()

    def _set_style(self):
        self.setStyleSheet(u"background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(184, 184, 184, 255),stop:1 rgba(209, 207, 207, 255));\n"
                            "")
        
    
    def _init_ui(self):
        self.scroll_panel = QtWidgets.QWidget()
        self.scroll_panel_layout = QFormLayout(self.scroll_panel)

        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidget(self.scroll_panel)

    def add_device(self, device: QtWidgets.QWidget):
        self.scroll_panel_layout.addWidget(device)
    
    def reseat(self):
        for i in reversed(range(self.scroll_panel_layout.count())): 
            self.scroll_panel_layout.itemAt(i).widget().deleteLater()

