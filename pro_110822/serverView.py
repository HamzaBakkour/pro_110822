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

from scrollArea import scrollPanel


class serverView(QtWidgets.QWidget):
    def __init__(self):        
        super(serverView, self).__init__()
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.setUpperFrame()
        self.serverInfoFram()
        self.connectedDevicesArea()



    def setUpperFrame(self):
        self.upperFrameLayout = QHBoxLayout()
        self.stopServerButton = QPushButton("Stop Server")
        self.upperFrameLayout.addWidget(self.stopServerButton)

        self.layout.addLayout(self.upperFrameLayout)


    def serverInfoFram(self):
        self.serverFrameLayout = QVBoxLayout()
        self.serverFrameLayout.addWidget(QLabel("Server Name : "))
        self.serverFrameLayout.addWidget(QLabel("Server IP        : "))

        self.layout.addLayout(self.serverFrameLayout)
  

    def connectedDevicesArea(self):
        self.connectedDevicesAreaLayout = QVBoxLayout()
        self.connectedDevices = scrollPanel()
        self.connectedDevicesAreaLayout.addWidget(QLabel("Connected Devices"))
        self.connectedDevicesAreaLayout.addWidget(self.connectedDevices)

        self.layout.addLayout(self.connectedDevicesAreaLayout)

    def remove(self):
        self.deleteLater()
