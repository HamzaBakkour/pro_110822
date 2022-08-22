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

        self.makeServerButton = QPushButton("Make Server")
        self.makeServerButton.setCheckable(True)
        self.refresh = QPushButton("Refresh")
        self.refresh.setCheckable(True)

        upperFrameLayout.addWidget(self.makeServerButton)
        upperFrameLayout.addWidget(self.refresh)
        self.layout.addLayout(upperFrameLayout)



    def setAvailableServersArea(self):
        availableServers = scrollPanel()
        self.layout.addWidget(availableServers)

    def remove(self):
        self.deleteLater()
