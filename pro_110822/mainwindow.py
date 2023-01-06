#pro_110822/mainWindow.py
"""
The programs main window module

CLASS MainWindow constins the following methods:
    - `__init__`
    - `on_shortcut_activate`
    - `define_shortcuts`
    - `_search_for_servers`
    - `_add_server`
    - `_establish_connection_to_server`
    - `_create_server`
    - `_handle_client_requests`
    - `_estaplish_connection_to_client`
    - `_add_client_widget`
    - `_close_server`
    - `_update_p_bar`
    - `_reseat_p_bar`

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

from PySide6 import QtWidgets
from pynput import keyboard

from clientview import ClientView
from serverview import ServerView
from serverworker import ServerWorker
from searchforserversworker import SearchForServersWorker
from progressbar import ProgressBar
from serverwidget import ServerWidget
from reciveuserinput import ReciveUserInput
from senduserinput import SendUserInput
from clientwidget import ClientWidget


import socket
import sys
import logging
import time
from ctypes import *
import os
import inspect

# import pdb
# pdb.post_mortem()
# pdb.set_trace()

#Creating and setting the format of the log file. 
logging.basicConfig(filename=(time.strftime("%Y%m%d---%H_%M_%S") + '.txt'), level=logging.DEBUG,
format="%(levelname)s\n%(asctime)s\n%(message)s", filemode="w")



class MainWindow(QMainWindow):
    def __init__(self, parent=None)-> None:
        super(MainWindow, self).__init__(parent)
        #Program title
        self.setWindowTitle("pro_110822")
        #Main window resulotion
        self.setFixedSize(600, 800)
        #Main window layout
        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.layout = QGridLayout()
        self.mainWidget.layout.setContentsMargins(0,0,0,0)
        self.mainWidget.layout.setSpacing(0)
        self.mainWidget.setLayout(self.mainWidget.layout)
        self.setCentralWidget(self.mainWidget)
        #Thread pool
        self.threabool = QThreadPool()
        self.threabool.setMaxThreadCount(20)
        #Start the program with ClientView
        self.mainWindowView = ClientView()
        self.mainWidget.layout.addWidget(self.mainWindowView)
        self.mainWindowView.makeServerButton.clicked.connect(self._create_server)
        self.mainWindowView.refreshButton.clicked.connect(self._search_for_servers)
        self.pBar = ProgressBar()
        self.mainWidget.layout.addWidget(self.pBar)
        self.pbarValue = 0
        #Variables used to handle connections
        self.clientsConnections = []
        self.serverWidget = None
        self.onShortcutActivateArgument = []
        self.sendUserInput = SendUserInput()
        #Define server shortcut
        self.connectionID = 1
        self.shortcutListner = False
        self.define_shortcuts('<ctrl>+m+' + str(self.connectionID), addToExist=False)   
        

    def on_shortcut_activate(self, m : str)-> None:
        """
        This method is called when a shortcut is pressed by the user.  
        Shortcuts are defind by the method define_shortcuts(self,*args, addToExist = False)

        Args:
            m: The shortcut that has been pressed by the user.

        Retursn:
            None
        """
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'shortcut detected >>> {m}')
        #Server shortcut
        if(m == '<ctrl>+m+1'):
            self.sendUserInput.supress_user_input(False)
            self.sendUserInput.send_input_to_client(None)
        else:#Client shortcut
            self.sendUserInput.supress_user_input(True)
            try:
                self.sendUserInput.send_input_to_client(self.clientsConnections[int(m[-1]) - 2])
            except Exception as ex:
                print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', ex)


    def define_shortcuts(self,*args : str, addToExist: bool = False) -> None:
        """
        Define shortcuts.  
        If a shortcut is pressed the method on_shortcut_activate is called and the
        shortcut is passed to it.

        Args:
            *args: Shortcuts that the listner will listen to.
            addToExist: If True, the shortcuts defined by args will be added to the existing shortcuts.  
                        If False,  any existing shortcuts will be removed and the shortcuts defined by args will be added.

        Returns:
            None
        """
        if (len(args) == 0):
            if self.shortcutListner:
                self.onShortcutActivateArgument = []
                self.shortcutListner.stop()
            return
        if (addToExist == False):
            argg = '{'
            for _ in range(len(args)):
                argg = argg + "'" + args[_] + "'" + ':' + ' lambda self = self : self.on_shortcut_activate({})'.format("'" + args[_] + "'") + ', '
            argg = argg[:-2] + '}'
            self.onShortcutActivateArgument = []
            self.onShortcutActivateArgument.extend(args)
        elif (addToExist == True):
            args = list(args)
            args.extend(self.onShortcutActivateArgument)
            argg = '{'
            for _ in range(len(args)):
                argg = argg + "'" + args[_] + "'" + ':' + ' lambda self = self : self.on_shortcut_activate({})'.format("'" + args[_] + "'") + ', '
            argg = argg[:-2] + '}'
            self.onShortcutActivateArgument = []
            self.onShortcutActivateArgument.extend(args)
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', '_define_shortcuts / args :', args)
        if self.shortcutListner:
            self.shortcutListner.stop()
            self.shortcutListner =  keyboard.GlobalHotKeys(eval(argg))
            self.shortcutListner.start()
        else:
            self.shortcutListner =  keyboard.GlobalHotKeys(eval(argg))
            self.shortcutListner.start()


    def _search_for_servers(self):
        """
        Starts the "search for servers worker"
        """
        self._reseat_p_bar()
        self.mainWindowView.availableServers.reseat()
        self._update_p_bar(15, "Searching for servers.")
        #Set the "search for servers worker"
        self.searchConntection = SearchForServersWorker(12345)
        #Connect the worker's connectionOkSignal signal to the function addServerToServersArea
        #The worker will send this signal to the main thread in case it manages to connect to a server on the local network
        self.searchConntection.signal.foundServer.connect(self._add_server)
        #The worker will send this signal to the main thread to update the progress bar when it manages to connect to a server on the local network
        self.searchConntection.signal.pbarSignal.connect(self._update_p_bar)
        #Start the woker
        self.threabool.start(self.searchConntection)


    def _add_server(self, serverName : str, serverIP: str, serverPort: int)-> None:
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "emited from searchForServers : ", serverName, serverIP)
        self.serverWidget = ServerWidget(serverName, serverIP)
        self.mainWindowView.add_deivce(self.serverWidget)
        self.serverWidget.connectToServer.clicked.connect(lambda: self._establish_connection_to_server(serverIP, serverPort))


    def _establish_connection_to_server(self ,serverIP: str, serverPort: int):
        if self.serverWidget.connectToServer.isChecked():
            self.serverWidget.connectToServer.setText('Disconnect')
            self.reciveMouseMovement = ReciveUserInput(serverIP, serverPort)
            self.threabool.start(self.reciveMouseMovement)
        else:
            self.serverWidget.connectToServer.setText('Connect')
            self.reciveMouseMovement.alive = False



    def _create_server(self):
        #Remove ClientView.
        self.mainWindowView.remove()
        self.pBar.remove()
        #Start ServerView.
        self.mainWindowView = ServerView()
        self.pBar = ProgressBar()
        self.mainWidget.layout.addWidget(self.mainWindowView)
        self.mainWidget.layout.addWidget(self.pBar)
        self.mainWindowView.stopServerButton.clicked.connect(self._close_server)
        #Create the server socket
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setblocking(False)
        self.serverSocket.bind(('', 12345))
        #Pass the server socket to ServerWorker
        self.serverWorker = ServerWorker(self.serverSocket)
        #Send clients requests to  _handle_client_requests
        self.serverWorker.signal.clientRequest.connect(self._handle_client_requests)
        self.threabool.start(self.serverWorker)
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
        self.define_shortcuts('<ctrl>+m+' + str(self.connectionID), addToExist=True)
        #Connect server to client
        self.clientsConnections.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        try:
            self.clientsConnections[-1].connect((clientIP, int(clientPort)))
        except Exception as ex:
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "Exception raised while server trying to connect to client.\nServer socket: {}\nCient IP: {}\nClient Port: {}\n\nException:\n{}".format(self.clientsConnections[-1], clientIP, clientPort, ex))
        #Add client widget to the UI
        self._add_client_widget(clientName, clientIP, self.clientsConnections[-1].getsockname()[1])


    def _add_client_widget(self, clientName, clientIP, clientPort):
        client = ClientWidget(clientName, clientIP, clientPort)
        self.mainWindowView.add_client(client)


    def _close_server(self):
        #Terminate serverWorker, serverSocket and user-input listner
        self.serverWorker.alive = False
        self.serverSocket.close()
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "Server Socket terminated")
        self.sendUserInput.stop_listning()
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "Input listner terminated")
        #Remove ServerView and set the new view to ClientView
        self.mainWindowView.remove()
        self.pBar.remove()
        self.mainWindowView = ClientView()
        self.pBar = ProgressBar()
        self.mainWidget.layout.addWidget(self.mainWindowView)
        self.mainWidget.layout.addWidget(self.pBar)
        self.mainWindowView.makeServerButton.clicked.connect(self._create_server)
        self.mainWindowView.refreshButton.clicked.connect(self._search_for_servers)


    def _update_p_bar(self, value, text):
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', text)
        if (value == 999):
            self._reseat_p_bar()
        else:
            self.pbarValue = self.pbarValue + value
            self.pBar.value(self.pbarValue)
            self.pBar.text(text)


    def _reseat_p_bar(self):
        self.pbarValue = 0
        self.pBar.reseat()


app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec())
