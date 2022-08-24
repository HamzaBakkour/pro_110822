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
        self.upperFrameLayout = QHBoxLayout()
        self.upperFrameLayout.addWidget(QLabel("Available servers"))

        self.makeServerButton = QPushButton("Make Server")
        self.makeServerButton.setCheckable(True)
        self.refreshButton = QPushButton("Refresh")
        self.refreshButton.setCheckable(True)

        self.upperFrameLayout.addWidget(self.makeServerButton)
        self.upperFrameLayout.addWidget(self.refreshButton)
        self.layout.addLayout(self.upperFrameLayout)



    def setAvailableServersArea(self):
        self.availableServers = scrollPanel()
        self.layout.addWidget(self.availableServers)

    def remove(self):
        self.deleteLater()
