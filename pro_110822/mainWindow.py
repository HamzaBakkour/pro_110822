#pro_110822/mainWindow.py
"""
The programs main window module

CLASS mainWindow constins the following methods:
    - `__init__`
    - `searchForServers`
    - `addServerToServersArea`
    - `createServer`
    - `establishConnectionToServer`
    - `closeServer`
    - `reseatAvaialbleServersArea`
    - `dataFromListningToConnectionsWorker`
    - `updatePbar`
    - `reseatPbar`
"""
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
from deviceWidget import device
from reciveMouseMovementWorker import reciveMouseMovementWorker

import socket

import sys
import os
import logging
import time

# import pdb
# pdb.post_mortem()
# pdb.set_trace()

#Creating and setting the format of the log file. 
logging.basicConfig(filename=(time.strftime("%Y%m%d---%H_%M_%S") + '.txt'), level=logging.DEBUG,
format="%(levelname)s\n%(asctime)s\n%(message)s", filemode="w")


class mainWindow(QMainWindow):
    def __init__(self, parent=None)-> None:
        """
        Constructor method.
        Initiate the main window.
        The main window is a supclass of `PySide6.QtWidgets.QMainWindow`
        """
        super(mainWindow, self).__init__(parent)
        #Main window title
        self.setWindowTitle("pro_110822")
        #Main window resulotion
        self.setFixedSize(600, 800)

        #Set the main window layout and widget
        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.layout = QGridLayout()
        self.mainWidget.layout.setContentsMargins(0,0,0,0)
        self.mainWidget.layout.setSpacing(0)
        self.mainWidget.setLayout(self.mainWidget.layout)
        self.setCentralWidget(self.mainWidget)

        #Craete a thread pool, will be used to spwan workers
        self.threabool = QThreadPool()

        #Start the main window with the firstOpenView view
        self.mainWindowView = firstOpenView()
        self.mainWidget.layout.addWidget(self.mainWindowView)
        #Connect the start server button to the funciton createServer
        self.mainWindowView.makeServerButton.clicked.connect(self.createServer)
        #Connect the refresh button to the funciton searchForServers
        self.mainWindowView.refreshButton.clicked.connect(self.searchForServers)

        #Set the progress bar
        self.pbarWidget = progressBar()
        self.mainWidget.layout.addWidget(self.pbarWidget)
        self.pbarValue = 0

        #This list is used to store XX 
        self.recivemouseMovementWorkers = []




    def searchForServers(self):
        """
        Search for available servers on the local network.
        """
        self.reseatPbar()
        self.reseatAvaialbleServersArea()
        self.updatePbar(15, "Searching for servers.")
        #Set the search for servers worker
        self.searchConntection = searchForServersWorker(12345)
        #Connect the worker's connectionOkSignal signal to the function addServerToServersArea
        #The worker will send this signal to the main thread in case it manages to connect to a server on the local network
        self.searchConntection.signal.connectionOkSignal.connect(self.addServerToServersArea)
        #The worker will send this signal to the main thread to update the progress bar when it manages to connect to a server on the local network
        self.searchConntection.signal.pbarSignal.connect(self.updatePbar)
        #Start the woker
        self.threabool.start(self.searchConntection)



    def addServerToServersArea(self, serverName : str, serverIP: str, serverPort: int)-> None:
        """
        Add a widget with the server name and IP to firstOpenView.
        This method is trigere by `searchForServers` method.

        Args:
            serverName
            serverIP
            serverPort
        """
        print("emited from searchForServers : ", serverName, serverIP)
        self.serverDevice1 = device(serverName, serverIP)
        self.mainWindowView.addDeivce(self.serverDevice1)
        self.serverDevice1.connectToServer.clicked.connect(lambda: self.establishConnectionToServer(serverIP, serverPort))




    def createServer(self):
        """
        Change the main window view from `firstOpenView` to `serverView`.
        Start the server worker.
        This worker will liten to connections on port `12345`.
        """
        #Remove the current view.
        self.mainWindowView.remove()
        self.pbarWidget.remove()
        #Set the view to serverView.
        self.mainWindowView = serverView()
        self.pbarWidget = progressBar()
        self.mainWidget.layout.addWidget(self.mainWindowView)
        self.mainWidget.layout.addWidget(self.pbarWidget)
        #Connect the server button to the fuction closeServer.
        self.mainWindowView.stopServerButton.clicked.connect(self.closeServer)
        #Set the server worker. This worker will listen for connection on the port 12345
        self.serverConnection = listenForConnectionsWorker(12345)
        #Connect the wroker's recivedConnection signal to the function  dataFromListningToConnectionsWorker
        self.serverConnection.signal.recivedConnection.connect(self.dataFromListningToConnectionsWorker)
        #Start the worker
        self.threabool.start(self.serverConnection)


    def establishConnectionToServer(self ,serverIP: str, serverPort: int):
        """
        Establish connection to server to get mouse movement.

        Args:
            serverIP
            serverPort
        """
        #Add a worker to the list recivemouseMovementWorkers.
        self.recivemouseMovementWorkers.append(reciveMouseMovementWorker(serverIP, serverPort))
        #Start the worker
        self.threabool.start(self.recivemouseMovementWorkers[-1])



    def closeServer(self):
        """
        Terminate the `listenForConnectionsWorker` worker.
        Change the main view from `serverView` to `firstOpenView`
        """
        self.serverConnection.terminate = True
        self.mainWindowView.remove()
        self.pbarWidget.remove()
        self.mainWindowView = firstOpenView()
        self.pbarWidget = progressBar()
        self.mainWidget.layout.addWidget(self.mainWindowView)
        self.mainWidget.layout.addWidget(self.pbarWidget)
        self.mainWindowView.makeServerButton.clicked.connect(self.createServer)
        self.mainWindowView.refreshButton.clicked.connect(self.searchForServers)



    def reseatAvaialbleServersArea(self):
        """
        Remove all the servers widges from `serverView`
        """
        self.mainWindowView.availableServers.reseat()



    def dataFromListningToConnectionsWorker(self, data : str):
        """
        XX
        """
        print("Recived from listenForConnectionsWorker")
        print("data: ", data)



    def updatePbar(self, value, text):
        """
        This method is triggered by `searchForServersWorker` worker.
        It updates the progress bar.
        """
        print(text)
        if (value == 999):
            self.reseatPbar()
        else:
            self.pbarValue = self.pbarValue + value
            self.pbarWidget.Value(self.pbarValue)
            self.pbarWidget.Text(text)


    def reseatPbar(self):
        """
        Reseat the progress bar.
        """
        self.pbarValue = 0
        self.pbarWidget.Reseat()







app = QApplication([])
window = mainWindow()
window.show()
sys.exit(app.exec())