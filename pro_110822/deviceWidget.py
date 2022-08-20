from xmlrpc.client import boolean
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
    def __init__(self,device_name: str, device_IP: list, its_the_host: boolean):        
        super(device, self).__init__()
        self.layout = QHBoxLayout(self)

        self.name = QLabel(device_name)
        self.address = QLabel(device_IP[0])

        self.layout.addWidget(self.name)
        self.layout.addWidget(self.address)

        if (its_the_host):
            self.its_me = QLabel('(This Device)')
            self.layout.addWidget(self.its_me)


        self.setLayout(self.layout)