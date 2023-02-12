from PySide6 import QtWidgets

from PySide6.QtWidgets import (
    QGridLayout,
    QLabel

)

from . import clientviewserverwidgetbtn1

class ServerWidget(QtWidgets.QFrame):
    def __init__(self, server_name: str, server_IP: list, *args, **kwargs):        
        super().__init__(*args, **kwargs)

        self.layout = QGridLayout(self)
        self.connectButton : QtWidgets.QPushButton
        self.serverName = server_name
        self.serverIP = server_IP
        self.setFixedHeight(75)

        self._init_ui()
        self._set_style()





    def _set_style(self):
        self.setStyleSheet("QFrame {background-color: #c9c9c9;"
                            "border-width: 1px;"
                            "border-radius: 10px;"
                            "border-top-right-radius: 0px;"
                            "border-style: inset;"
                            "border-color: #787777;}"

                            "QLabel {background-color: #c9c9c9;"
                            "border: none;}"

                           )
    def _init_ui(self):
        leftGrid = QGridLayout()
        rightGrid = QGridLayout()

        self.layout.setSpacing(0)
        self.layout.setColumnStretch(0,3)
        self.layout.setColumnStretch(1,1)



        self.connectButton = clientviewserverwidgetbtn1.ClientViewServerWidgetBtn1()
        self.connectButton.set_text('Connect')
        
        rightGrid.addWidget(QLabel(), 0, 0)
        rightGrid.addWidget(self.connectButton, 1, 0)
        leftGrid.addWidget(QLabel('Server name: ' + self.serverName))
        leftGrid.addWidget(QLabel('Server IP: ' + self.serverIP))




        self.layout.addLayout(leftGrid, 0, 0)
        self.layout.addLayout(rightGrid, 0, 1)










    







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



