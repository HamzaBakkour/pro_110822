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
        self.layout = QHBoxLayout(self)
        device_nanme_and_ip_layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()

        connect = QPushButton("Connect")
        disconnect = QPushButton("Disconnect")
        make_server =  QPushButton("Make Server")


        if (device_name[-5:] == ".home"):
            self.name = QLabel(device_name[:-5])
        else:
            self.name = QLabel(device_name)
        
        self.address = QLabel(device_IP[0])

        device_nanme_and_ip_layout.addWidget(self.name)
        device_nanme_and_ip_layout.addWidget(self.address)


        self.layout.addLayout(device_nanme_and_ip_layout)
        if (device_name[-5:] == ".home"):
            self.layout.addWidget(QLabel("(This device)"))
        else:
            buttons_layout.addWidget(make_server)
        buttons_layout.addWidget(connect)
        buttons_layout.addWidget(disconnect)
        

        self.layout.addLayout(buttons_layout)


        self.setLayout(self.layout)