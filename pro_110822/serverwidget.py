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

class ServerWidget(QtWidgets.QFrame):
    def __init__(self,device_name: str, device_IP: list):        
        super(ServerWidget, self).__init__()

        #Set the class layout
        self.setObjectName("ParentWidget");
        self.layout = QHBoxLayout(self)
        self.setStyleSheet("QWidget#ParentWidget {background-color: white; margin:5px; border:1px solid black;}")
        self.setLayout(self.layout)

        #Set a VBox layout for the name and the ip
        device_nanme_and_ip_layout = QVBoxLayout()

        name = QLabel("Server name : " + device_name)
        address = QLabel("Server IP        : " + device_IP)
        #Add the device name and IP to the VBox layout 
        device_nanme_and_ip_layout.addWidget(name)
        device_nanme_and_ip_layout.addWidget(address)
        self.layout.addLayout(device_nanme_and_ip_layout)

        self.buttons_layout = QHBoxLayout()
        self.connectToServer = QPushButton("Connect")
        self.buttons_layout.addWidget(self.connectToServer)
        self.layout.addLayout(self.buttons_layout)




