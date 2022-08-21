from email.charset import QP
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

class device(QtWidgets.QWidget):
    def __init__(self,device_name: str, device_IP: list):        
        super(device, self).__init__()

        #Set the class layout
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)

        #Set a VBox layout for the name and the ip
        device_nanme_and_ip_layout = QVBoxLayout()
        if (device_name[-5:] == ".home"):
            name = QLabel(device_name[:-5])
        else:
            name = QLabel(device_name)
        address = QLabel(device_IP[0])
        #Add the device name and IP to the VBox layout 
        device_nanme_and_ip_layout.addWidget(name)
        device_nanme_and_ip_layout.addWidget(address)
        #Add the VBox layout to the widget layout
        self.layout.addLayout(device_nanme_and_ip_layout)

        #If the device name ends with .home add (This deivce) label to the widget main layout
        if (device_name[-5:] == ".home"):
            self.layout.addWidget(QLabel("(This device)"))


        #Init the buttons layout -> at the begning it contains only connect button
        self.initButtonsLayouts()




    def initButtonsLayouts(self):
        #Set the buttons layout to HBox
        self.buttons_layout = QHBoxLayout()
        #Add connect button the HBox
        self.addConnectButton()
        self.layout.addLayout(self.buttons_layout)


    def addConnectButton(self):
        connect = QPushButton("Connect")
        self.buttons_layout.addWidget(connect)

    def addDisconnecteButton(self):
        disconnect = QPushButton("Disconnect")
        self.buttons_layout.addWidget(disconnect)

    def addMakeServerButton(self):
        make_server =  QPushButton("Make Server")
        self.buttons_layout.addWidget(make_server)
