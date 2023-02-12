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
# from qt_material import apply_stylesheet
from pynput import keyboard

from client_view import clientview
from server_view import serverview
from serverworker import ServerWorker
from searchforserversworker import SearchForServersWorker
from reciveuserinput import ReciveUserInput
from senduserinput import SendUserInput
from clientwidget import ClientWidget
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


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs)-> None:
        super().__init__(*args, **kwargs)
        #Program title
        self.setWindowTitle("pro_110822")


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
        self.clientsConnections = []
        self.clientWidgets = []
        self.serverWidget = None
        self.connectionsMonitor = ConnectionsMonitor(self.clientsConnections)
        self.connectionsMonitor.signal.socketError.connect(self._remove_client_widget)


        self.connectionID = 1
        self.sendUserInput = SendUserInput()
        self.sendUserInput.signal.socketTerminated.connect(self._remove_client_widget)


        self.shortcutHandle = ShortcutsHandle(self)
        self.shortcutHandle.define_shortcut(('<ctrl>+m+1', '_unsupress_user_input'), addToExist=False, passShortcut=False)


        self.clientView.upperFrame.searchButton.clicked.connect(self.clientView.scrollArea.reseat)

        self.clientView.upperFrame.createButton.clicked.connect(lambda port = 12345 : self._create_server(port))
        self.clientView.upperFrame.searchButton.clicked.connect(lambda port = 12345 : self._search_for_servers(port))



    def _search_for_servers(self, serverPort):
        searchForServersWorker = SearchForServersWorker(serverPort)
        searchForServersWorker.signal.infoSignal.connect(self._update_client_view_progress_bar)
        searchForServersWorker.signal.foundServer.connect(self._add_server)
        self.threabool.start(searchForServersWorker)

    def _update_client_view_progress_bar(self, progressBarValue, progressBarMessage):
        if (progressBarValue == 999):
            pass
        elif (progressBarValue < 101):
            self.clientView.bottomFrame.brogressBar.setValue(progressBarValue)
        else:
            print(f'Search for servers worker reported a progress value of {progressBarValue}!!!')
        self.clientView.bottomFrame.info_text(progressBarMessage)


    def _add_server(self, serverName : str, serverIP: str, serverPort: int)-> None:
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "emited from searchForServers : ", serverName, serverIP)
        self.serverWidget = ServerWidget(serverName, serverIP)
        self.mainWindowView.add_deivce(self.serverWidget)
        self.serverWidget.connectToServer.clicked.connect(lambda: self._establish_connection_to_server(serverIP, serverPort))

#asd
    def _establish_connection_to_server(self ,serverIP: str, serverPort: int):
        if self.serverWidget.connectToServer.isChecked():
            self.serverWidget.connectToServer.setText('Disconnect')
            self.reciveMouseMovement = ReciveUserInput(serverIP, serverPort)
            self.threabool.start(self.reciveMouseMovement)
        else:
            self.serverWidget.connectToServer.setText('Connect')
            self.reciveMouseMovement.alive = False



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
        self.threabool.start(self.connectionsMonitor)
        #Start listning for user input
        self.sendUserInput.start_listning()


    def _handle_client_requests(self, data : str):
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "Recived client request : ", data)
        try:
            if (data.split('!')[0] == 'C'):#'C' stands for Connection requst
                                            #Connection requsts format "C!CLIENT_SCREEN_W!CLIENT_SCREEN_H!CLIENT_PORT!CLIENT_NAME!CLIENT_IP"
                CLIENT_SCREEN_W = data.split('!')[1]
                CLIENT_SCREEN_H = data.split('!')[2]
                CLIENT_PORT = data.split('!')[3]
                CLIENT_NAME = data.split('!')[4]
                CLIENT_IP = data.split('!')[5]
        except Exception as ex:
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "Exception raised while handling client requst.\nRequst data:\n{}\n\Exception:\n{}".format(data, ex))
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
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "Exception raised while server trying to connect to client.\nServer socket: {}\nCient IP: {}\nClient Port: {}\n\nException:\n{}".format(self.clientsConnections[-1], clientIP, clientPort, ex))
        #Monitor the connection
        self.connectionsMonitor.connectionsList = self.clientsConnections
        #Add client widget to the UI
        self._add_client_widget(clientName, clientIP, self.clientsConnections[-1][0].getsockname()[1], shortcut)



    def _unsupress_user_input(self):
        self.sendUserInput.supress_user_input(False)
        self.sendUserInput.send_input_to_client(None)     



    def _switch_input_to_client(self, shortcutPressed):
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', '_switch_input_to_client')
        self.sendUserInput.supress_user_input(True)
        try:
            self.sendUserInput.send_input_to_client(self.clientsConnections[int(shortcutPressed[-1]) - 2][0])
        except Exception as ex:
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Exception raisde {ex}')





    def _add_client_widget(self, clientName, clientIP, clientPort, shortcut):
        self.clientWidgets.append(ClientWidget(clientName, clientIP, clientPort, shortcut))
        self.mainWindowView.add_client(self.clientWidgets[-1])


    def _close_server(self):
        #Terminate serverWorker, serverSocket and user-input listner
        self.serverWorker.alive = False
        self.serverSocket.close()
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "Server Socket terminated")
        self.sendUserInput.stop_listning()
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "Input listner terminated")
        self.connectionsMonitor.alive = False
        #Remove ServerView and set the new view to ClientView
        self.mainWindowView.remove()
        self.pBar.remove()
        self.mainWindowView = ClientView()
        self.pBar = ProgressBar()
        self.mainWidget.layout.addWidget(self.mainWindowView)
        self.mainWidget.layout.addWidget(self.pBar)
        self.mainWindowView.makeServerButton.clicked.connect(self._create_server)
        self.mainWindowView.refreshButton.clicked.connect(self._search_for_servers)




    def _remove_client_widget(self, socketPort):
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Client socket terminated {socketPort}')
        for widget in self.clientWidgets:
            if (widget.port == socketPort):
                widget.deleteLater()
                self.shortcutHandle.remove_shortcut(widget.shortcut)

                

app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec())