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

from scrollArea import scrollPanel


class firstOpenView(QtWidgets.QWidget):
    def __init__(self):        
        super(firstOpenView, self).__init__()
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.setUpperFrame()
        self.setAvailableServersArea()




    def setUpperFrame(self):
        upperFrameLayout = QHBoxLayout()
        upperFrameLayout.addWidget(QLabel("Available servers"))

        makeServerButton = QPushButton("Make Server")
        makeServerButton.setCheckable(True)
        makeServerButton.clicked.connect(self.makeServer)

        upperFrameLayout.addWidget(makeServerButton)
        self.layout.addLayout(upperFrameLayout)



    def setAvailableServersArea(self):
        availableServers = scrollPanel()
        self.layout.addWidget(availableServers)

    def makeServer(self):
        print("Creating Server")
        return("Server")