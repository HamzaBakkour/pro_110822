import sys
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QApplication, QFormLayout, QScrollArea, QGridLayout, QPushButton


class ScrollPanelWidget(QScrollArea):

    def __init__(self, parent= None):
        super().__init__()
        self.initUI()
    
    def initUI(self):

        # widgets
        self.scroll_panel = QtWidgets.QWidget()
        self.scroll_panel_layout = QFormLayout(self.scroll_panel)
        self.scroll_panel_layout.setContentsMargins(0,0,0,0)

        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidget(self.scroll_panel)

        # layout
        # self.mainLayout = QGridLayout(self)
        # self.mainLayout.setContentsMargins(0,0,0,0)
        # self.mainLayout.addWidget(self.scroll_area)


        for i in range(20):
            btn = QPushButton("test")
            self.scroll_panel_layout.addWidget(btn)

        # self.show()