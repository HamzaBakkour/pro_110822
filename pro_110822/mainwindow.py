#pro_110822/mainWindow.py
"""
The program's main window module
"""
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QThreadPool, SIGNAL
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QGridLayout,
    QStackedWidget,
    QVBoxLayout,
    QLabel
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
import struct


#Creating and setting the format of the log file. 
# logging.basicConfig(filename=(time.strftime("%Y%m%d---%H_%M_%S") + '.txt'), level=logging.DEBUG,
# format="%(levelname)s\n%(asctime)s\n%(message)s", filemode="w")



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
        self.threabool.setMaxThreadCount(25)



        #Variables used to handle connections
        self.clientWidgets = []
        self.serverWidgets = []
        self.connectionsID = []
        self.reciveMouseMovementWorkers = []
        self.serverWidgetID = 0
        self.serverWidget : QtWidgets.QFrame
        self.connections = []
        self.connectionsMonitor = ConnectionsMonitor(self.connections)
        self.connectionsMonitor.connectionsList = self.connections
        self.connectionsMonitor.signal.socketError.connect(self._remove_client_widget)
        self.threabool.start(self.connectionsMonitor)


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

    def _add_server(self, serverName : str, serverIP: str, serverPort: int)-> None:
        self.serverWidgets.append(serverwidget.ServerWidget(serverName, serverIP, serverPort))
        self.clientView.scrollArea.add_device(self.serverWidgets[-1])
        self.serverWidgetID = self.serverWidgetID + 1
        localID = self.serverWidgetID
        self.serverWidgets[-1].connectButton.clicked.connect(lambda: self._connect__disconnect_to_server(serverIP, serverPort, localID))


    def _connect__disconnect_to_server(self ,serverIP: str, serverPort: int, id):
        if(self.serverWidgets[id-1].connectButton.isChecked()):
            self.serverWidgets[id-1].connectButton.change_style_on_checked(True)
            self.reciveMouseMovementWorkers.append(ReciveUserInput(serverIP, serverPort, id))
            self.reciveMouseMovementWorkers[-1].signal.serverStoped.connect(self._remove_server_widget)
            self.threabool.start(self.reciveMouseMovementWorkers[-1])
        else:
            self.serverWidgets[id-1].connectButton.change_style_on_checked(False)
            for worker in self.reciveMouseMovementWorkers:
                if (worker.id == id):
                    worker.alive = False

    def _remove_server_widget(self, serverConnection, id, port):
        for widget in self.serverWidgets:
            if (widget.port == port):
                try:
                    widget.deleteLater()
                    serverConnection.close()
                except RuntimeError:#Delete a widget that already has been deleted
                    print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', 'RuntimeError (widget already deleted) -> passed')
                    pass
                except Exception as ex:
                    print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Exception raisde {ex}')


    def _create_server(self, serverPort):
        for connection in self.connections:
            connection.close()
        for widget in self.serverWidgets:
            try:
                widget.deleteLater()
            except RuntimeError:#Delete a widget that already has been deleted
                print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', 'RuntimeError (widget already deleted) -> passed')
                pass
            except Exception as ex:
                print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Exception raisde {ex}')    

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setblocking(False)
        self.serverSocket.bind(('', serverPort))
        self.serverWorker = ServerWorker(self.serverSocket)
        self.serverWorker.signal.clientRequest.connect(self._handle_client_requests)
        self.threabool.start(self.serverWorker)
        self.sendUserInput.start_listning()
        self.Stack.setCurrentIndex(1)




    def _unsupress_user_input(self):
        self.sendUserInput.supress_user_input(False)
        self.sendUserInput.send_input_to_client(None)     

    def _switch_input_to_client(self, shortcutPressed):
        self.sendUserInput.supress_user_input(True)
        try:
            for connection in self.connections:
                if connection['shortcut'] == shortcutPressed:
                    self.sendUserInput.send_input_to_client(connection['connection'])
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
            print(f'[*]{os.path.basename(__file__)} || ', f'{inspect.stack()[0][3]} || ', "Exception raised while handling client requst.\nRequst data:\n{}\n\Exception:\n{}".format(data, ex))
        self._estaplish_connection_to_client((CLIENT_SCREEN_W, CLIENT_SCREEN_H), CLIENT_IP, CLIENT_PORT, CLIENT_NAME)



    def _estaplish_connection_to_client(self, clientScreenResolution : tuple, clientIP : str, clientPort : str, clientName : str):
        
        okNumber = False
        for n in range (2, 9):
            if (n not in self.connectionsID):
                self.connectionsID.append(n)
                okNumber = True
                break

        if (not okNumber):
            tempLable = QLabel('Maximun number of clients (8) has been reached!')
            tempLable.setStyleSheet("background-color: #f07269")
            tempLable.setAlignment(QtCore.Qt.AlignCenter)
            self.serverView.scrollArea.add_device(tempLable)
            return

        shortcut = '<ctrl>+m+' + str(self.connectionsID[-1])
        self.shortcutHandle.define_shortcut((shortcut, '_switch_input_to_client'), addToExist=True, passShortcut=True)
        
        # self.clientsConnections.append(((socket.socket(socket.AF_INET, socket.SOCK_STREAM), shortcut), self.connectionID))
        self.connections.append({'connection' : socket.socket(socket.AF_INET, socket.SOCK_STREAM), 'shortcut' : shortcut})

        try:
            self.connections[-1]['connection'].connect((clientIP, int(clientPort)))
        except Exception as ex:
            print(f'[*]{os.path.basename(__file__)} || ', f'{inspect.stack()[0][3]} || ', f'{inspect.stack()[1][3]} || ', f"Exception raised while server trying to connect to client.\nCient IP: {clientIP}\nClient Port: {clientPort}\n\nException:\n{ex}")
        try:
            self._add_client_widget(clientName, clientIP, self.connections[-1]['connection'].getsockname()[1], shortcut, self.connectionsID[-1])
        except IndexError as ie:
            print(f'[*]{os.path.basename(__file__)} || ', f'{inspect.stack()[0][3]} || ', f'{inspect.stack()[1][3]} || ', f"Endex error while trying to add client : {clientName}, with ip : {clientIP} and shortcut : {shortcut}\n{ie}")


    def _add_client_widget(self, clientName, clientIP, clientPort, shortcut, connectionID):
        self.clientWidgets.append(clientwidget.ClientWidget(clientName, clientIP, clientPort, shortcut, connectionID))
        self.serverView.scrollArea.add_device(self.clientWidgets[-1])


    def _remove_client_widget(self, socketPort):
        for widget in self.clientWidgets:
            if (widget.port == socketPort):
                print(f'removed widgt with the id {widget.id}')
                self.connectionsID.remove(widget.id)
                widget.deleteLater()
                self.shortcutHandle.remove_shortcut(widget.shortcut)


    def _close_server(self):
        self.serverWorker.alive = False
        self.serverSocket.close()
        print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "Server Socket terminated")
        self.sendUserInput.stop_listning()
        print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "Input listner terminated")

        for connection in self.connections:
            message = 'SS'.encode()
            header = struct.pack('<L', len(message))
            connection['connection'].sendall(header + message)

        self.Stack.setCurrentIndex(0)

                

app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec())