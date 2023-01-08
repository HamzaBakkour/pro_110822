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
    def __init__(self,clientName: str, clientIP: list, clientPort : int, shortcut : str):        
        super(ClientWidget, self).__init__()

        #Set the class layout
        self.setObjectName("ParentWidget");
        self.layout = QHBoxLayout(self)
        self.setStyleSheet("QWidget#ParentWidget {background-color: white; margin:5px; border:1px solid black;}")
        self.setLayout(self.layout)
        self.port = clientPort
        self.shortcut = shortcut
        self._build_ui(clientName, clientIP, clientPort, shortcut)

    def _build_ui(self, clientName, clientIP, clientPort, shortcut):

            #Set a VBox layout for the name and the ip
            clientInfoLayout = QVBoxLayout()

            name = QLabel("Client name : " + clientName)
            ip = QLabel("Client IP        : " + clientIP)
            port = QLabel("Connected via port        : " + str(clientPort))
            shortcut = QLabel("Shortcut        : " + shortcut)

            #Add the device name and IP to the VBox layout 
            clientInfoLayout.addWidget(name)
            clientInfoLayout.addWidget(ip)
            clientInfoLayout.addWidget(port)
            clientInfoLayout.addWidget(shortcut)


            self.layout.addLayout(clientInfoLayout)





