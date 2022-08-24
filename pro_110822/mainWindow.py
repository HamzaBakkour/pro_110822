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
from serverWorkers import listenForConnectionsWorker
from searchForServersWorker import searchForServersWorker

import sys
import socket

class mainWindow(QMainWindow):

    def __init__(self, parent=None):
        #init the main window
        super(mainWindow, self).__init__(parent)
        self.setWindowTitle("pro_110822")
        self.setFixedSize(600, 800)

        #Set the main window widget
        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.layout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainWidget.layout)
        self.setCentralWidget(self.mainWidget)

        #Craeting a thread pool for the main window class
        self.threabool = QThreadPool()

        #Starting the main window with the firstOpenView view
        self.mainWindowView = firstOpenView()
        self.mainWidget.layout.addWidget(self.mainWindowView)
        self.mainWindowView.makeServerButton.clicked.connect(self.createServer)
        self.mainWindowView.refreshButton.clicked.connect(self.searchForServers)
        # self.searchForServers()


    def searchForServers(self):
        self.searchConntection = searchForServersWorker(12345)
        self.searchConntection.signal.sendSignal.connect(self.poo_2)
        self.threabool.start(self.searchConntection)
        
    def poo_2(self, server : list)-> None:
        print(server)



    def createServer(self):
        self.mainWindowView.remove()
        self.mainWindowView = serverView()
        self.mainWidget.layout.addWidget(self.mainWindowView)
        self.mainWindowView.stopServerButton.clicked.connect(self.closeServer)

        self.serverConnection = listenForConnectionsWorker(12345)
        self.serverConnection.signal.sendSignal.connect(self.poo)
        self.threabool.start(self.serverConnection)
        print("Created Server")


    def closeServer(self):
        self.serverConnection.terminate = True
        self.mainWindowView.remove()
        self.mainWindowView = firstOpenView()
        self.mainWidget.layout.addWidget(self.mainWindowView)
        self.mainWindowView.makeServerButton.clicked.connect(self.createServer)
        self.mainWindowView.refreshButton.clicked.connect(self.searchForServers)

    


    def poo(self, socket: socket.socket, addr: tuple):
        print(socket)
        print(addr)


app = QApplication([])
window = mainWindow()
window.show()
sys.exit(app.exec_())