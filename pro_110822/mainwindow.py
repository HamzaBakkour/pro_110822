#pro_110822/mainWindow.py
"""
The program's main window module
"""
from PySide6 import QtWidgets
from PySide6.QtCore import QThreadPool, SIGNAL
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QGridLayout,
    QStackedWidget,
    QVBoxLayout
)


from PySide6 import QtWidgets
from pynput import keyboard

from client_view import clientview, serverwidget
from server_view import serverview, clientwidget

from serverworker import ServerWorker
from searchforserversworker import SearchForServersWorker
from reciveuserinput import ReciveUserInput
from senduserinput import SendUserInput
from connectionsmonitor import ConnectionsMonitor
from shortcuthandle import ShortcutsHandle


import socket
import sys
import logging
import time
from ctypes import *
import os
import inspect


#Creating and setting the format of the log file. 
# logging.basicConfig(filename=(time.strftime("%Y%m%d---%H_%M_%S") + '.txt'), level=logging.DEBUG,
# format="%(levelname)s\n%(asctime)s\n%(message)s", filemode="w")

"""
Problem is:

      SERVER                               CLIENT
*connection monitor*                      [connect]

when the client connect the first tinme and then disconnect
the connection monitor detect that the connection was closed
and it removes the client widget.
after the first connection. if the client connect and disconnect,
connection monitor is not detecting that the connection is closed.

so, the problem is in the client -> starts at the connect/disconnect button.
"""



class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs)-> None:
        super().__init__(*args, **kwargs)
        #Program title
        self.setWindowTitle("pro_110822")

        self.searchOngoning = False

        self.clientView = clientview.ClientView()
        self.serverView = serverview.ServerView()


        #Main window resulotion
        self.setMinimumSize(200, 200)
        self.setMaximumSize(500, 800)
        self.resize(600, 600)
        
        self.Stack = QStackedWidget(self)

        self.setCentralWidget(self.Stack)

        self.Stack.addWidget(self.clientView)
        self.Stack.addWidget(self.serverView)
        self.Stack.setCurrentIndex(0)


        #Thread pool
        self.threabool = QThreadPool()
        self.threabool.setMaxThreadCount(20)



        #Variables used to handle connections
        self.clientWidgets = []
        self.serverWidgets = []
        self.reciveMouseMovementWorkers = []
        self.serverWidgetID = 0
        self.serverWidget : QtWidgets.QFrame
        self.clientsConnections = []
        self.connectionsMonitor = ConnectionsMonitor(self.clientsConnections)
        self.connectionsMonitor.connectionsList = self.clientsConnections
        self.connectionsMonitor.signal.socketError.connect(self._remove_client_widget)
        self.threabool.start(self.connectionsMonitor)


        self.connectionID = 1
        self.sendUserInput = SendUserInput()
        self.sendUserInput.signal.socketTerminated.connect(self._remove_client_widget)


        self.shortcutHandle = ShortcutsHandle(self)
        self.shortcutHandle.define_shortcut(('<ctrl>+m+1', '_unsupress_user_input'), addToExist=False, passShortcut=False)


        self.clientView.upperFrame.createButton.clicked.connect(lambda : self._create_server(12345) if (not self.searchOngoning) else ())
        self.clientView.upperFrame.searchButton.clicked.connect(lambda:  self.clientView.scrollArea.reseat() if (not self.searchOngoning) else ())
        self.clientView.upperFrame.searchButton.clicked.connect(lambda : self._search_for_servers(12345) if (not self.searchOngoning) else ())
        self.serverView.upperFrame.stopButton.clicked.connect(lambda: self._close_server())


        # self._add_server('TEST-SERVER1', '111.999.999.999', 10000)
        # self._add_server('TEST-SERVER2', '222.999.999.999', 10000)
        # self._add_server('TEST-SERVER3', '333.999.999.999', 10000)
        # self._add_server('TEST-SERVER4', '444.999.999.999', 10000)

    def _search_for_servers(self, serverPort):
        searchForServersWorker = SearchForServersWorker(serverPort)
        searchForServersWorker.signal.infoSignal.connect(self._update_client_view_progress_bar)
        searchForServersWorker.signal.foundServer.connect(self._add_server)
        self.threabool.start(searchForServersWorker)


    def _update_client_view_progress_bar(self, progressBarValue, progressBarMessage):
        if (progressBarValue > 0):
            self.searchOngoning = True
        if(progressBarValue == 999):
            self.searchOngoning = False

        self.clientView.bottomFrame.brogressBar.setValue(progressBarValue)
        self.clientView.bottomFrame.info_text(progressBarMessage)

################################################################################################################################################
    def _add_server(self, serverName : str, serverIP: str, serverPort: int)-> None:
        self.serverWidgets.append(serverwidget.ServerWidget(serverName, serverIP))
        self.clientView.scrollArea.add_device(self.serverWidgets[-1])
        self.serverWidgetID = self.serverWidgetID + 1
        localID = self.serverWidgetID
        print(f'self.serverWidgetID : {self.serverWidgetID}')
        print(f'localID : {localID}')
        self.serverWidgets[-1].connectButton.clicked.connect(lambda: self._connect__disconnect_to_server(serverIP, serverPort, localID))


    def _connect__disconnect_to_server(self ,serverIP: str, serverPort: int, id):
        print(f'[X][X][X][X]From _connect__disconnect_to_server. serverIP : {serverIP}, serverPort : {serverPort}, id : {id}, self.serverWidgets[id-1].connectButton.isChecked() : {self.serverWidgets[id-1].connectButton.isChecked()}')
        if(self.serverWidgets[id-1].connectButton.isChecked()):
            self.serverWidgets[id-1].connectButton.change_style_on_checked(True)
            self.reciveMouseMovementWorkers.append(ReciveUserInput(serverIP, serverPort, id))
            self.threabool.start(self.reciveMouseMovementWorkers[-1])
        else:
            print(f'[X] Removing reciveMouseMovementWorkers with id : {id}, id-1 : {id-1}')
            self.serverWidgets[id-1].connectButton.change_style_on_checked(False)
            for worker in self.reciveMouseMovementWorkers:
                if (worker.id == id):
                    worker.alive = False
            # self.reciveMouseMovementWorkers[id-1].alive = False
################################################################################################################################################

    def _create_server(self, serverPort):
        self.Stack.setCurrentIndex(1)
        #Create the server socket
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setblocking(False)
        self.serverSocket.bind(('', serverPort))
        #Pass the server socket to ServerWorker
        self.serverWorker = ServerWorker(self.serverSocket)
        #Send clients requests to  _handle_client_requests
        self.serverWorker.signal.clientRequest.connect(self._handle_client_requests)
        self.threabool.start(self.serverWorker)
        #Start listning for user input
        self.sendUserInput.start_listning()



    def _unsupress_user_input(self):
        self.sendUserInput.supress_user_input(False)
        self.sendUserInput.send_input_to_client(None)     

    def _switch_input_to_client(self, shortcutPressed):
        print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', '_switch_input_to_client')
        self.sendUserInput.supress_user_input(True)
        try:
            self.sendUserInput.send_input_to_client(self.clientsConnections[int(shortcutPressed[-1]) - 2][0])
        except Exception as ex:
            print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Exception raisde {ex}')





    def _handle_client_requests(self, data : str):
        print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "Recived client request : ", data)
        try:
            if (data.split('!')[0] == 'C'):#'C' stands for Connection requst
                                            #Connection requsts format "C!CLIENT_SCREEN_W!CLIENT_SCREEN_H!CLIENT_PORT!CLIENT_NAME!CLIENT_IP"
                CLIENT_SCREEN_W = data.split('!')[1]
                CLIENT_SCREEN_H = data.split('!')[2]
                CLIENT_PORT = data.split('!')[3]
                CLIENT_NAME = data.split('!')[4]
                CLIENT_IP = data.split('!')[5]
        except Exception as ex:
            print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "Exception raised while handling client requst.\nRequst data:\n{}\n\Exception:\n{}".format(data, ex))
        self._estaplish_connection_to_client((CLIENT_SCREEN_W, CLIENT_SCREEN_H), CLIENT_IP, CLIENT_PORT, CLIENT_NAME)

    def _estaplish_connection_to_client(self, clientScreenResolution : tuple, clientIP : str, clientPort : str, clientName : str):
        #Define client shortcut
        self.connectionID = self.connectionID + 1
        shortcut = '<ctrl>+m+' + str(self.connectionID)
        self.shortcutHandle.define_shortcut((shortcut, '_switch_input_to_client'), addToExist=True, passShortcut=True)
        
        #Connect server to client
        self.clientsConnections.append((socket.socket(socket.AF_INET, socket.SOCK_STREAM), self.connectionID))
        try:
            self.clientsConnections[-1][0].connect((clientIP, int(clientPort)))
        except Exception as ex:
            print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "Exception raised while server trying to connect to client.\nServer socket: {}\nCient IP: {}\nClient Port: {}\n\nException:\n{}".format(self.clientsConnections[-1], clientIP, clientPort, ex))
        #Monitor the connection
        #Add client widget to the UI
        self._add_client_widget(clientName, clientIP, self.clientsConnections[-1][0].getsockname()[1], shortcut)

    def _add_client_widget(self, clientName, clientIP, clientPort, shortcut):
        self.clientWidgets.append(clientwidget.ClientWidget(clientName, clientIP, clientPort, shortcut))
        # self.mainWindowView.add_client(self.clientWidgets[-1])
        self.serverView.scrollArea.add_device(self.clientWidgets[-1])

    def _remove_client_widget(self, socketPort):
        print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Client socket terminated {socketPort}')
        for widget in self.clientWidgets:
            if (widget.port == socketPort):
                widget.deleteLater()
                self.shortcutHandle.remove_shortcut(widget.shortcut)


    def _close_server(self):
        #Terminate serverWorker, serverSocket and user-input listner
        self.serverWorker.alive = False
        self.serverSocket.close()
        print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "Server Socket terminated")
        self.sendUserInput.stop_listning()
        print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "Input listner terminated")
        self.Stack.setCurrentIndex(0)

                

app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec())