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

from . import clientviewserverwidgetbtn1

class ServerWidget(QtWidgets.QFrame):
    def __init__(self, server_name: str, server_IP: list):        
        super(ServerWidget, self).__init__()

        self.layout = QGridLayout(self)
        self.connectButton : QtWidgets.QPushButton
        self.serverName = server_name
        self.serverIP = server_IP
        self._set_style()
        self._init_ui()
        # self.setFixedHeight(100)



    def _set_style(self):
        self.setStyleSheet(u"background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.100559 rgba(216, 216, 216, 255), stop:0.849162 rgba(226, 226, 226, 255));\n"
                            "border-radius: 2px;\n"
                            "\n"
                            "")


    def _init_ui(self):
        leftGrid = QGridLayout()
        rightGrid = QGridLayout()

        # self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,1)

        self.connectButton = clientviewserverwidgetbtn1.ClientViewServerWidgetBtn1()
        self.connectButton.set_text('Connect')
        
        rightGrid.addWidget(self.connectButton,0,0)
        leftGrid.addWidget(QLabel(self.serverName))
        leftGrid.addWidget(QLabel(self.serverIP))




        self.layout.addLayout(leftGrid, 0, 0)
        self.layout.addLayout(rightGrid, 0, 1)


        # self.layout.setRowStretch(1,30)
        # self.layout.setRowStretch(2,1)






    







# class ServerWidget(QtWidgets.QFrame):
#     def __init__(self,device_name: str, device_IP: list):        
#         super(ServerWidget, self).__init__()

#         #Set the class layout
#         self.setObjectName("ParentWidget");
#         self.layout = QHBoxLayout(self)
#         self.setStyleSheet("QWidget#ParentWidget {background-color: white; margin:5px; border:1px solid black;}")
#         self.setLayout(self.layout)

#         #Set a VBox layout for the name and the ip
#         device_nanme_and_ip_layout = QVBoxLayout()

#         name = QLabel("Server name : " + device_name)
#         address = QLabel("Server IP        : " + device_IP)
#         #Add the device name and IP to the VBox layout 
#         device_nanme_and_ip_layout.addWidget(name)
#         device_nanme_and_ip_layout.addWidget(address)
#         self.layout.addLayout(device_nanme_and_ip_layout)

#         self.buttons_layout = QHBoxLayout()
#         self.connectToServer = QPushButton("Connect")
#         self.connectToServer.setCheckable(True)
#         self.buttons_layout.addWidget(self.connectToServer)
#         self.layout.addLayout(self.buttons_layout)



