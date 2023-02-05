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

# from scrollarea import ScrollPanel


class ServerView(QtWidgets.QWidget):
    def __init__(self):        
        super(ServerView, self).__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10,30,10,0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.set_upper_frame()
        self.server_info_fram()
        self.connected_devices_area()



    def set_upper_frame(self):
        self.upperFrameLayout = QHBoxLayout()
        self.stopServerButton = QPushButton("Stop Server")
        self.upperFrameLayout.addWidget(self.stopServerButton)

        self.layout.addLayout(self.upperFrameLayout)


    def server_info_fram(self):
        self.serverFrameLayout = QVBoxLayout()
        self.serverFrameLayout.addWidget(QLabel("Server Name : "))
        self.serverFrameLayout.addWidget(QLabel("Server IP        : "))

        self.layout.addLayout(self.serverFrameLayout)
  

    def connected_devices_area(self):
        self.connectedDevicesAreaLayout = QVBoxLayout()
        self.connectedDevices = ScrollPanel()
        self.connectedDevicesAreaLayout.addWidget(QLabel("Connected Devices"))
        self.connectedDevicesAreaLayout.addWidget(self.connectedDevices)

        self.layout.addLayout(self.connectedDevicesAreaLayout)

    def add_client(self, client):
        self.connectedDevices.add_device(client)
        pass



    def remove(self):
        self.deleteLater()
