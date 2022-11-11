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
from pynput import keyboard

from firstopenview import FirstOpenView
from serverview import ServerView
from listenforconnectionsworker import ListenForConnectionsWorker
from searchforserversworker import SearchForServersWorker
from progressbar import ProgressBar
from devicewidget import Device
from recivemousemovementworker import ReciveMouseMovementWorker
from sendmousemovement2 import SendMouseKeyboard



import socket

import sys
import struct
import os
import logging
import time

# import pdb
# pdb.post_mortem()
# pdb.set_trace()

#Creating and setting the format of the log file. 
logging.basicConfig(filename=(time.strftime("%Y%m%d---%H_%M_%S") + '.txt'), level=logging.DEBUG,
format="%(levelname)s\n%(asctime)s\n%(message)s", filemode="w")


class MainWindow(QMainWindow):
    def __init__(self, parent=None)-> None:
        super(MainWindow, self).__init__(parent)

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
        self.threabool.setMaxThreadCount(12)

        #Start the main window with the firstOpenView view
        self.mainWindowView = FirstOpenView()
        self.mainWidget.layout.addWidget(self.mainWindowView)
        #Connect the start server button to the funciton createServer
        self.mainWindowView.makeServerButton.clicked.connect(self.create_server)
        #Connect the refresh button to the funciton searchForServers
        self.mainWindowView.refreshButton.clicked.connect(self.search_for_servers)

        #Set the progress bar
        self.pbarWidget = ProgressBar()
        self.mainWidget.layout.addWidget(self.pbarWidget)
        self.pbarValue = 0

        #This list is used to store sending mouse movmement sockets
        self.sendmouseMovmentSockets = []


        #############################
        self.sendMouseKeyboard = SendMouseKeyboard()
        self.sendMouseKeyboard.start_listning()
        

        #shortcuts listner  
        self.listner = False
        self._define_shortcuts('<ctrl>+m+1')      


    def _on_shortcut_activate(self, m):
        print(f'shortcut detected >>> {m}')
        print("111")
        print("passed {}".format(self.sendmouseMovmentSockets[0]))
        print("222")
        self.sendMouseKeyboard.set_active_connection(self.sendmouseMovmentSockets[-1]['socket'])
        

    def _define_shortcuts(self, *args):

        def get_count_of_shortcuts():
            n = 0
            for _ in args:
                n = n + 1
            return n

        count = get_count_of_shortcuts()

        argg = '{'
        for _ in range(count):
            argg = argg + "'" + args[_] + "'" + ':' + ' lambda self = self : self._on_shortcut_activate({})'.format("'" + args[_] + "'") + ', '

        argg = argg[:-2] + '}'

        if self.listner:
            self.listner.stop()
            self.listner =  keyboard.GlobalHotKeys(eval(argg))
            self.listner.start()
        else:
            self.listner =  keyboard.GlobalHotKeys(eval(argg))
            self.listner.start()


##################################################################################################################################################################
    def search_for_servers(self):
        self.reseat_p_bar()
        self.reseat_avaialble_servers_area()
        self.update_p_bar(15, "Searching for servers.")
        #Set the search for servers worker
        self.searchConntection = SearchForServersWorker(12345)
        #Connect the worker's connectionOkSignal signal to the function addServerToServersArea
        #The worker will send this signal to the main thread in case it manages to connect to a server on the local network
        self.searchConntection.signal.foundServer.connect(self.add_server_to_servers_area)
        #The worker will send this signal to the main thread to update the progress bar when it manages to connect to a server on the local network
        self.searchConntection.signal.pbarSignal.connect(self.update_p_bar)
        #Start the woker
        self.threabool.start(self.searchConntection)

    def add_server_to_servers_area(self, serverName : str, serverIP: str, serverPort: int)-> None:
        print("emited from searchForServers : ", serverName, serverIP)
        self.serverWidget = Device(serverName, serverIP)
        self.mainWindowView.add_deivce(self.serverWidget)
        self.serverWidget.connectToServer.clicked.connect(lambda: self.establish_connection_to_server(serverIP, serverPort))

    def establish_connection_to_server(self ,serverIP: str, serverPort: int):
        self.reciveMouseMovement = ReciveMouseMovementWorker(serverIP, serverPort)
        self.threabool.start(self.reciveMouseMovement)


##################################################################################################################################################################

    def create_server(self):
        #Remove the current view.
        self.mainWindowView.remove()
        self.pbarWidget.remove()
        #Set the view to serverView.
        self.mainWindowView = ServerView()
        self.pbarWidget = ProgressBar()
        self.mainWidget.layout.addWidget(self.mainWindowView)
        self.mainWidget.layout.addWidget(self.pbarWidget)
        #Connect the server button to the fuction closeServer.
        self.mainWindowView.stopServerButton.clicked.connect(self.close_server)

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setblocking(False)
        self.serverSocket.bind(('', 12345))

        #Set the server worker. This worker will listen for connection on the port 12345
        self.listningConnection = ListenForConnectionsWorker(self.serverSocket)


        #Connect the wroker's recivedConnection signal to the function  dataFromListningToConnectionsWorker
        self.listningConnection.signal.connectionFromClient.connect(self.data_from_listning_to_connections_worker)

        #Start the worker
        
        self.threabool.start(self.listningConnection)


    def close_server(self):
        self.listningConnection.terminate = True
        try:
            self.listningConnection.serverSocket.close()
            self.listningConnection.serverInfoToClientSocket.close()
            print("Connected Socket terminated")
        except :#trying to close c before any connections are acepted
                            # trying to close a connection that does not exist -> AttributeError
                            # occures when try to close the server before any connections are accepted
                            # part1 = str(sys.exc_info())

            print("Not Connected Socket terminated")
        self.mainWindowView.remove()
        self.pbarWidget.remove()
        self.mainWindowView = FirstOpenView()
        self.pbarWidget = ProgressBar()
        self.mainWidget.layout.addWidget(self.mainWindowView)
        self.mainWidget.layout.addWidget(self.pbarWidget)
        self.mainWindowView.makeServerButton.clicked.connect(self.create_server)
        self.mainWindowView.refreshButton.clicked.connect(self.search_for_servers)



    def reseat_avaialble_servers_area(self):
        self.mainWindowView.availableServers.reseat()



    def data_from_listning_to_connections_worker(self, data : str):
        print("Emited from ListenForConnectionsWorker -> MainWindow : ", data)
        dataType = data.split('!')[0]

        if (dataType == 'C'):
            clientScreenRezW = data.split('!')[1]
            clientScreenRezH = data.split('!')[2]
            clientReceiveSocketPort = data.split('!')[3]
            clientReceiveSocketIP = data.split('!')[4]
            self.create_sending_socket((clientScreenRezW, clientScreenRezH), clientReceiveSocketIP, clientReceiveSocketPort)

        # print("{} : {} : {} : {} : {}".format(dataType, clientScreenRezW, clientScreenRezH, clientReceiveSocketPort, clientReceiveSocketIP))




    def create_sending_socket(self, ReseiveRez : tuple, receiveIP : str, receivePort : str):
        receivePort = int(receivePort)
        self.sendmouseMovmentSockets.append({'socket': socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                                            'shortcut' : '<ctrl>+m+1'})
        self.sendmouseMovmentSockets[-1]['socket'].connect((receiveIP, receivePort))
        


    def update_p_bar(self, value, text):
        print(text)
        if (value == 999):
            self.reseat_p_bar()
        else:
            self.pbarValue = self.pbarValue + value
            self.pbarWidget.value(self.pbarValue)
            self.pbarWidget.text(text)


    def reseat_p_bar(self):
        self.pbarValue = 0
        self.pbarWidget.reseat()



app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec())