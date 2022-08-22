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
        upperFrameLayout = QHBoxLayout()
        self.stopServerButton = QPushButton("Stop Server")
        upperFrameLayout.addWidget(self.stopServerButton)

        self.layout.addLayout(upperFrameLayout)


    def serverInfoFram(self):
        serverFrameLayout = QVBoxLayout()
        serverFrameLayout.addWidget(QLabel("Server Name : "))
        serverFrameLayout.addWidget(QLabel("Server IP        : "))

        self.layout.addLayout(serverFrameLayout)
  

    def connectedDevicesArea(self):
        connectedDevicesAreaLayout = QVBoxLayout()
        connectedDevices = scrollPanel()
        connectedDevicesAreaLayout.addWidget(QLabel("Connected Devices"))
        connectedDevicesAreaLayout.addWidget(connectedDevices)

        self.layout.addLayout(connectedDevicesAreaLayout)

    def remove(self):
        self.deleteLater()
