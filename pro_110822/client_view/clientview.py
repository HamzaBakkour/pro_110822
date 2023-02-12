#pro_110822/firstOpenView.py

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


from . import clientviewupperframe
from . import clientviewscrollarea
from . import clientviewbuttomframe
from . import serverwidget
<<<<<<< HEAD
# from . import serverwidget_old
=======
from . import serverwidget_old
>>>>>>> b04d7d4cc4a07e99918ac70c6b9d380a9e62ae72



class ClientView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
<<<<<<< HEAD
        super().__init__(*args, **kwargs)
        self.upperFrame = clientviewupperframe.ClientViewUpperFrame()
        self.scrollArea = clientviewscrollarea.ClientViewScrollArea()
        self.bottomFrame = clientviewbuttomframe.ClientViewBottomFrame()
=======
        super(ClientView, self).__init__(*args, **kwargs)
        self.upperFrame = clientviewupperframe.ClientViewUpperFrame()
        self.scrollArea = clientviewscrollarea.ClientViewScrollArea()
        self.buttomFrame = clientviewbuttomframe.ClientViewButtomFrame()
>>>>>>> b04d7d4cc4a07e99918ac70c6b9d380a9e62ae72
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(0)

        self.layout.setRowStretch(0,5)
        self.layout.setRowStretch(1,30)
        self.layout.setRowStretch(2,1)
<<<<<<< HEAD
=======

        self.layout.addWidget(self.upperFrame, 0, 0)
        self.layout.addWidget(self.scrollArea, 1, 0)
        self.layout.addWidget(self.buttomFrame, 2, 0)
        self.scrollArea.add_device(serverwidget.ServerWidget('QT-TEST1-1001_PRO110822', ('255.255.255.255')))
        self.scrollArea.add_device(serverwidget.ServerWidget('QT-TEST2-1001_PRO110822', ('255.255.255.255')))
        # self.scrollArea.add_device(serverwidget.ServerWidget('QT-TEST3-1001_PRO110822', ('255.255.255.255')))
        # self.scrollArea.add_device(serverwidget_old.ServerWidget('QT-TEST1-1001_PRO110822', ('255.255.255.255')))
        # self.scrollArea.add_device(serverwidget_old.ServerWidget('QT-TEST2-1001_PRO110822', ('255.255.255.255')))

        


>>>>>>> b04d7d4cc4a07e99918ac70c6b9d380a9e62ae72

        self.layout.addWidget(self.upperFrame, 0, 0)
        self.layout.addWidget(self.scrollArea, 1, 0)
        self.layout.addWidget(self.bottomFrame, 2, 0)




        self.scrollArea.add_device(serverwidget.ServerWidget('QT-TEST1-1001_PRO110822', ('255.255.255.255')))
        self.scrollArea.add_device(serverwidget.ServerWidget('QT-TEST2-1001_PRO110822', ('255.255.255.255')))
        # self.scrollArea.add_device(serverwidget.ServerWidget('QT-TEST3-1001_PRO110822', ('255.255.255.255')))
        # self.scrollArea.add_device(serverwidget_old.ServerWidget('QT-TEST1-1001_PRO110822', ('255.255.255.255')))
        # self.scrollArea.add_device(serverwidget_old.ServerWidget('QT-TEST2-1001_PRO110822', ('255.255.255.255')))

        






  































    # def __init__(self):
    #     super(ClientView, self).__init__()
    #     self.layout = QVBoxLayout(self)
        
    #     # self.layout.setContentsMargins(10,30,10,0)
    #     self.layout.setSpacing(0)
    #     self.setLayout(self.layout)
    #     self.set_upper_frame()
    #     self.set_available_servers_area()
    #     self.setObjectName('Widget1')
    #     self.setStyleSheet(Stylesheet)



    # def set_upper_frame(self):
    #     self.upperFrameLayout = QHBoxLayout()#(left, top, right, bottom)
    #     # self.upperFrameLayout.setObjectName('Widget1')
    #     self.upperFrameLayout.setContentsMargins(0,   0,   0,     60)
    #     self.upperFrameLayout.addWidget(QLabel("Available servers"))

    #     self.makeServerButton = QPushButton("Make Server")
    #     # self.makeServerButton.setObjectName('Widget1')
    #     self.makeServerButton.setCheckable(True)
    #     self.refreshButton = QPushButton("Refresh")
    #     self.refreshButton.setCheckable(True)

    #     self.upperFrameLayout.addWidget(self.makeServerButton)
    #     self.upperFrameLayout.addWidget(self.refreshButton)
    #     self.layout.addLayout(self.upperFrameLayout)



    # def set_available_servers_area(self):
    #     self.availableServers = ScrollPanel()
    #     # self.availableServers.setContentsMargins(10,30,10,0)
    #     self.layout.addWidget(self.availableServers)

    # def add_deivce(self, device: QtWidgets.QWidget):
    #     self.availableServers.add_device(device)


    # def remove(self):
    #     self.deleteLater()



# Stylesheet = """
# create_server_button 
# {
# 	background-color: transparent;
# 	color: #fff;
# 	padding: 5px;
# 	padding-left: 8px;
# 	padding-right: 8px;
# 	margin-left: 1px;
# }
# create_server_button:hover
# {
# 	background-color: rgba(183, 134, 32, 20%);
# 	border: 1px solid #b78620;
# 	color: #fff;
	
# }
# create_server_button:pressed
# {
# 	background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(57, 57, 57, 255),stop:1 rgba(50, 50, 50, 255));
# 	border: 1px solid #b78620;
# }

# """


	# color: #fff;
	# selection-background-color: #b78620;
	# selection-color: #000;
    # border: none;       

# #closeButton {
#     min-width: 36px;
#     min-height: 36px;
#     font-family: "Webdings";
#     qproperty-text: "r";
#     border-radius: 10px;
# }
# #closeButton:hover {
#     color: #ccc;
#     background: red;
# }