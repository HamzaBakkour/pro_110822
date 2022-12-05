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

class ClientWidget(QtWidgets.QFrame):
    def __init__(self,clientName: str, clientIP: list, clientPort):        
        super(ClientWidget, self).__init__()

        #Set the class layout
        self.setObjectName("ParentWidget");
        self.layout = QHBoxLayout(self)
        self.setStyleSheet("QWidget#ParentWidget {background-color: white; margin:5px; border:1px solid black;}")
        self.setLayout(self.layout)

        #Set a VBox layout for the name and the ip
        clientInfoLayout = QVBoxLayout()

        clientName = QLabel("Client name : " + clientName)
        ClientIP = QLabel("Client IP        : " + clientIP)
        ClientPort = QLabel("Connected via port        : " + str(clientPort))
        #Add the device name and IP to the VBox layout 
        clientInfoLayout.addWidget(clientName)
        clientInfoLayout.addWidget(ClientIP)
        clientInfoLayout.addWidget(ClientPort)

        self.layout.addLayout(clientInfoLayout)

        # self.buttons_layout = QHBoxLayout()
        # self.connectToServer = QPushButton("Connect")
        # self.buttons_layout.addWidget(self.connectToServer)
        # self.layout.addLayout(self.buttons_layout)




