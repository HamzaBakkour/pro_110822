#pro_110822/firstOpenView.py
"""
The programs main window module

CLASS firstOpenView constins the following methods:
    - `__init__`
    - `setUpperFrame`
    - `setAvailableServersArea`
    - `addDevice`
"""

from PySide6 import QtCore, QtWidgets

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QScrollArea,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel
)

from scrollarea import ScrollPanel

class FirstOpenView(QtWidgets.QWidget):
    def __init__(self):
        super(FirstOpenView, self).__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10,30,10,0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.set_upper_frame()
        self.set_available_servers_area()


    def set_upper_frame(self):
        self.upperFrameLayout = QHBoxLayout()
        self.upperFrameLayout.addWidget(QLabel("Available servers"))

        self.makeServerButton = QPushButton("Make Server")
        self.makeServerButton.setCheckable(True)
        self.refreshButton = QPushButton("Refresh")
        self.refreshButton.setCheckable(True)

        self.upperFrameLayout.addWidget(self.makeServerButton)
        self.upperFrameLayout.addWidget(self.refreshButton)
        self.layout.addLayout(self.upperFrameLayout)



    def set_available_servers_area(self):
        self.availableServers = ScrollPanel()
        self.layout.addWidget(self.availableServers)

    def add_deivce(self, device: QtWidgets.QWidget):
        self.availableServers.addDevice(device)


    def remove(self):
        self.deleteLater()
