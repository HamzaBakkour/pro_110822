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
from connection import mouseAndKeyboardConnection
from serverWorkers import listenForConnectionsWorker

import sys
import signal
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
        self.mainWindowView.makeServerButton.clicked.connect(self.makeServer)



    def searchForServers(self):
        pass



    def makeServer(self):
        self.mainWindowView.remove()
        self.mainWindowView = serverView()
        self.mainWidget.layout.addWidget(self.mainWindowView)

        self.connection = listenForConnectionsWorker(12345)
        self.connection.signal.sendSignal.connect(self.poo)
        self.threabool.start(self.connection)
        print("Created Server")

    def closeServer(self):
        self.connection.terminate = True
    


    def poo(self, socket: socket.socket, addr: tuple):
        print(socket)
        print(addr)
        self.closeServer()

    # def searchForAvialableServers(self)-> dict:
    #     pass

app = QApplication([])
window = mainWindow()
window.show()
sys.exit(app.exec_())