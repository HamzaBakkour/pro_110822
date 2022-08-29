from PySide6 import QtCore, QtWidgets

from PySide6.QtCore import QThreadPool

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QScrollArea,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel
)

from PySide6 import QtGui, QtCore, QtWidgets

from firstOpenView import firstOpenView
from serverView import serverView
from listenForConnectionsWorker import listenForConnectionsWorker
from searchForServersWorker import searchForServersWorker
from progressBar import progressBar

import socket

import sys
import os
import logging
import time

# import pdb
# pdb.post_mortem()
# pdb.set_trace()


logging.basicConfig(filename=(time.strftime("%Y%m%d---%H_%M_%S") + '.txt'), level=logging.DEBUG,
format="%(levelname)s\n%(asctime)s\n%(message)s", filemode="w")


class mainWindow(QMainWindow):

    def __init__(self, parent=None):
        #init the main window
        super(mainWindow, self).__init__(parent)
        self.setWindowTitle("pro_110822")
        self.setFixedSize(600, 800)

        #Set the main window widget
        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.layout = QGridLayout()
        self.mainWidget.layout.setContentsMargins(0,0,0,0)
        self.mainWidget.layout.setSpacing(0)

        self.mainWidget.setLayout(self.mainWidget.layout)
        self.setCentralWidget(self.mainWidget)

        #Craeting a thread pool for the main window class
        self.threabool = QThreadPool()

        #Starting the main window with the firstOpenView view
        self.mainWindowView = firstOpenView()
        self.mainWidget.layout.addWidget(self.mainWindowView)
        self.mainWindowView.makeServerButton.clicked.connect(self.createServer)
        self.mainWindowView.refreshButton.clicked.connect(self.searchForServers)

        #Set the progress bar
        self.pbarWidget = progressBar()
        self.mainWidget.layout.addWidget(self.pbarWidget)
        self.pbarValue = 0


    def searchForServers(self):
        self.reseatPbar()
        self.updatePbar(15, "Searching for servers.")
        self.searchConntection = searchForServersWorker(12345)
        self.searchConntection.signal.sendSignal.connect(self.poo_2)
        self.searchConntection.signal.pbarSignal.connect(self.updatePbar)
        self.threabool.start(self.searchConntection)

        

        

    def poo_2(self, device : list)-> None:
        # print("emoted from searchForServers : ", device)
        pass


    def updatePbar(self, value, text):
        print(text)
        if (value == 999):
            self.reseatPbar()
        else:
            self.pbarValue = self.pbarValue + value
            self.pbarWidget.Value(self.pbarValue)
            self.pbarWidget.Text(text)


    def reseatPbar(self):
        self.pbarValue = 0
        self.pbarWidget.Reseat()

    def createServer(self):
        self.mainWindowView.remove()
        self.pbarWidget.remove()
        self.mainWindowView = serverView()
        self.pbarWidget = progressBar()
        self.mainWidget.layout.addWidget(self.mainWindowView)
        self.mainWidget.layout.addWidget(self.pbarWidget)
        self.mainWindowView.stopServerButton.clicked.connect(self.closeServer)
        self.serverConnection = listenForConnectionsWorker(12345)
        self.serverConnection.signal.sendSignal.connect(self.poo)
        self.threabool.start(self.serverConnection)


    def poo(self, socket: socket.socket, addr: tuple):
        print("Server recived connection request from")
        print(addr)


    def closeServer(self):
        self.serverConnection.terminate = True
        self.mainWindowView.remove()
        self.pbarWidget.remove()
        self.mainWindowView = firstOpenView()
        self.pbarWidget = progressBar()
        self.mainWidget.layout.addWidget(self.mainWindowView)
        self.mainWidget.layout.addWidget(self.pbarWidget)
        self.mainWindowView.makeServerButton.clicked.connect(self.createServer)
        self.mainWindowView.refreshButton.clicked.connect(self.searchForServers)

    



app = QApplication([])
window = mainWindow()
window.show()
sys.exit(app.exec())