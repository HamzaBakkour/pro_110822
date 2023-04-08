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

import threading
import time



from client_view.clientview import ClientView 
from client_view.serverwidget import ServerWidget
from client_view.serverwidget import  ServerWidget

from server_view.serverview import ServerView
from server_view.clientwidget import ClientWidget


from client.reciveuserinput import ReciveUserInput
from client.searchforserversworker import SearchForServersWorker

from server.server import Server
from server.server import ServerSignals
from server.senduserinput import SendUserInput
from server.shortcuthandle import ShortcutsHandle

from client.client import Client
from client.client import ClientSignals

import sys
import pdb



#Creating and setting the format of the log file. 
# logging.basicConfig(filename=(time.strftime("%Y%m%d---%H_%M_%S") + '.txt'), level=logging.DEBUG,
# format="%(levelname)s\n%(asctime)s\n%(message)s", filemode="w")



class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs)-> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle("pro_110822")
        self.setMinimumSize(200, 200)
        self.setMaximumSize(500, 800)
        self.resize(600, 600)


        #Server variables
        self.serverView = ServerView()
        self.connectedClientss = []
        self._clientsWidgets = []
        self._server = None
        self._serverSignals = None

        #Client variables
        self.clientView = ClientView()
        self._clientViewWidgets = []
        self._client = None
        self._clientSignals = None
        # self._connected_servers = []
       

        self._stack = QStackedWidget(self)
        self.setCentralWidget(self._stack)
        self._stack.addWidget(self.clientView)
        self._stack.addWidget(self.serverView)
        self.set_view('CLIENT')

        self._threabool = QThreadPool()
        self._threabool.setMaxThreadCount(25)

        self._connect_buttons()




    def _connect_buttons(self):
        self.clientView.upperFrame.createButton.clicked.connect(lambda : self.start_server())
        self.clientView.upperFrame.searchButton.clicked.connect(lambda:  self._search_for_servers(8888))
        # self.clientView.upperFrame.searchButton.clicked.connect(lambda : self._search_for_servers(12345) if (not self.searchOngoning) else ())
        self.serverView.upperFrame.stopButton.clicked.connect(lambda: self.close_server())

    def boo(self, connected_clients):
        print(f"boo {connected_clients}")

    def boo2(self):
        pass        

    def set_view(self, view):
        if (view == 'SERVER'):
            self._stack.setCurrentIndex(1)
        elif(view == 'CLIENT'):
            self._clear_server_view()
            self._stack.setCurrentIndex(0)
        else:
            print(f"{view} is unknown view name.")

    def start_server(self):
        self.set_view('SERVER')
        self._init_server('192.168.0.107', 8888)
        self._threabool.start(self._server)
        self._threabool.start(self._serverSignals)

    def _init_server(self, serverIP, serverPort):
        self._server = Server(serverIP, serverPort)
        self._serverSignals = ServerSignals()
        self._serverSignals.signals.server_view_maneger.connect(self._server_view_add_remove_client_widget)
        self._serverSignals.signals.recived_messages.connect(self.boo2)

    def _server_view_add_remove_client_widget(self):
        for client in self._server.connected_clients:
                if (not self._has_widget(client)):
                    print(f'\n mainwindow, _server_view_add_remove_client_widget, _create_widget ' \
                          f'was called with client:{client}')
                    if (len(client[2]) < 1):
                        print(f'\nmainwindow, _server_view_add_remove_client_widget, client:{client} '\
                              f'did not report resolution to the server yet, skipped.')    
                        continue
                    self._create_widget(client)
        
        for widget in self._clientsWidgets:
            if (not self._still_connected(widget)):
                self._remove_widget(widget)
                self._clientsWidgets.remove(widget)

    def _has_widget(self, client):
        for widget in self._clientsWidgets:
            if ((client[0][0] == widget.ip) and (client[0][1] == widget.port) and (len(client[2]) > 1)):
                return True
        return False

    def _create_widget(self, client):
        self._clientsWidgets.append(ClientWidget(client))
        self.serverView.scrollArea.add_device(self._clientsWidgets[-1])

    def _still_connected(self, widget):
        for client in self._server.connected_clients:
            if ((client[0][0], client[0][1]) == (widget.ip, widget.port)):
                return True
        return False

    def _remove_widget(self, widget):
        widget.deleteLater()

    def start_client(self):
        self.set_view('CLIENT')
        self._client = Client('192.168.0.107', 8888)
        self._clientSignals = ClientSignals(self._client.recived_messages)
        self._threabool.start(self._client)
        self._threabool.start(self._clientSignals)

    def _clear_server_view(self):
        for widget in self._clientsWidgets:
            widget.deleteLater()
            self._clientsWidgets.remove(widget)

    def close_server(self):
        self._server.close_server()
        self._serverSignals.alive = False
        self.set_view('CLIENT')
        

    def _search_for_servers(self, serverPort):
        search = SearchForServersWorker(serverPort)
        search.signal.infoSignal.connect(self._client_view_progress_bar)
        search.signal.foundServer.connect(self._client_view_add_server)
        self._threabool.start(search)

    def _client_view_progress_bar(self, progressBarValue, progressBarMessage):
        self.clientView.bottomFrame.brogressBar.setValue(progressBarValue)
        self.clientView.bottomFrame.info_text(progressBarMessage)


    def _client_view_add_server(self, serverName : str, serverIP: str, serverPort: int)-> None:
        if self.clientView.widget_already_exist(serverIP, serverPort):
            print(f"\nmainwindow, _client_view_add_server, server:{serverIP}:{serverPort}, already exist, returning...")
            return
        print(f"\nmainwindow, _client_view_add_server, adding widget for server:{serverIP}:{serverPort}")
        self.clientView.add_widget(ServerWidget(serverName, serverIP, serverPort))
        self.clientView.last_added_widget.connectButton.clicked.connect(lambda: self._server_connection(serverIP, serverPort))


    def _server_connection(self ,serverIP: str, serverPort: int):
        print(f'\nmainwindow, _server_connection, called with server:{serverIP}:{serverPort}')

        for server_widget in self.clientView.widgets:
            if (server_widget.serverIP == serverIP) and (server_widget.port == serverPort):
                print(f'\nmainwindow, _server_connection,  server_widget.connected:{server_widget.connected}')
                if server_widget.connected:
                    print(f"DISSONNECTIN FROM SERVER {serverIP}:{serverPort}")
                    self._disconnect_from_server()
                    server_widget.connected = False
                else:
                    print(f"CONNECTING TO SERVER {serverIP}:{serverPort}")
                    self._connect_to_server(serverIP, serverPort)
                    server_widget.connected = True



    def _connect_to_server(self, serverIP, serverPort):
            if self._client != None:
                print(f'\nmainwindow, _connect_to_server, cannot connect to server:{serverIP}:{serverPort}' 
                      '\n client already connected, RETURNING...')
                return
            self._client = Client(serverIP, serverPort)
            self._clientSignals = ClientSignals(self._client.recived_messages)
            self._threabool.start(self._client)
            self._threabool.start(self._clientSignals)


    def _disconnect_from_server(self):
        if self._client == None:
            print('\nmainwindow, _disconnect_from_server, client is already disconnected, RETURNING...')
            return
        self._client.close_connection()
        self._client = None
        self._clientSignals.alive = False



    def _remove_server_widget(self, serverConnection, id, port):
        print('')
        # for widget in self.serverWidgets:
        #     if (widget.port == port):
        #         try:
        #             widget.deleteLater()
        #             serverConnection.close()
        #         except RuntimeError:#Delete a widget that already has been deleted
        #             print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', 'RuntimeError (widget already deleted) -> passed')
                    
        #         except Exception as ex:
        #             print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Exception raisde {ex}')

    def _unsupress_user_input(self):
        print('')
        # self.sendUserInput.supress_user_input(False)
        # self.sendUserInput.send_input_to_client(None)     

    def _switch_input_to_client(self, shortcutPressed):
        print('')
        # self.sendUserInput.supress_user_input(True)
        # try:
        #     for connection in self.connections:
        #         if connection['shortcut'] == shortcutPressed:
        #             self.sendUserInput.send_input_to_client(connection['connection'])
        # except Exception as ex:
        #     print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Exception raisde {ex}')

    def _handle_client_requests(self, data : str):
        print('')
        # print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "Recived client request : ", data)
        # try:
        #     if (data.split('!')[0] == 'C'):#'C' stands for Connection requst
        #                                     #Connection requsts format "C!CLIENT_SCREEN_W!CLIENT_SCREEN_H!CLIENT_PORT!CLIENT_NAME!CLIENT_IP"
        #         CLIENT_SCREEN_W = data.split('!')[1]
        #         CLIENT_SCREEN_H = data.split('!')[2]
        #         CLIENT_PORT = data.split('!')[3]
        #         CLIENT_NAME = data.split('!')[4]
        #         CLIENT_IP = data.split('!')[5]
        # except Exception as ex:
        #     print(f'[*]{os.path.basename(__file__)} || ', f'{inspect.stack()[0][3]} || ', "Exception raised while handling client requst.\nRequst data:\n{}\n\Exception:\n{}".format(data, ex))
        # self._estaplish_connection_to_client((CLIENT_SCREEN_W, CLIENT_SCREEN_H), CLIENT_IP, CLIENT_PORT, CLIENT_NAME)

    def _estaplish_connection_to_client(self, clientScreenResolution : tuple, clientIP : str, clientPort : str, clientName : str):
        print('')
        
        # okNumber = False
        # for n in range (2, 9):
        #     if (n not in self.connectionsID):
        #         self.connectionsID.append(n)
        #         okNumber = True
        #         break

        # if (not okNumber):
        #     tempLable = QLabel('Maximun number of clients (8) has been reached!')
        #     tempLable.setStyleSheet("background-color: #f07269")
        #     tempLable.setAlignment(QtCore.Qt.AlignCenter)
        #     self.serverView.scrollArea.add_device(tempLable)
        #     return

        # shortcut = '<ctrl>+m+' + str(self.connectionsID[-1])
        # self.shortcutHandle.define_shortcut((shortcut, '_switch_input_to_client'), addToExist=True, passShortcut=True)
        
        # # self.clientsConnections.append(((socket.socket(socket.AF_INET, socket.SOCK_STREAM), shortcut), self.connectionID))
        # self.connections.append({'connection' : socket.socket(socket.AF_INET, socket.SOCK_STREAM), 'shortcut' : shortcut})

        # try:
        #     self.connections[-1]['connection'].connect((clientIP, int(clientPort)))
        # except Exception as ex:
        #     print(f'[*]{os.path.basename(__file__)} || ', f'{inspect.stack()[0][3]} || ', f'{inspect.stack()[1][3]} || ', f"Exception raised while server trying to connect to client.\nCient IP: {clientIP}\nClient Port: {clientPort}\n\nException:\n{ex}")
        # try:
        #     self._add_client_widget(clientName, clientIP, self.connections[-1]['connection'].getsockname()[1], shortcut, self.connectionsID[-1])
        # except IndexError as ie:
        #     print(f'[*]{os.path.basename(__file__)} || ', f'{inspect.stack()[0][3]} || ', f'{inspect.stack()[1][3]} || ', f"Endex error while trying to add client : {clientName}, with ip : {clientIP} and shortcut : {shortcut}\n{ie}")

    def _add_client_widget(self, clientName, clientIP, clientPort, shortcut, connectionID):
        print('')
        # self.clientWidgets.append(clientwidget.ClientWidget(clientName, clientIP, clientPort, shortcut, connectionID))
        # self.serverView.scrollArea.add_device(self.clientWidgets[-1])

    def _remove_client_widget(self, socketPort):
        print('')
        # for widget in self.clientWidgets:
        #     if (widget.port == socketPort):
        #         print(f'removed widgt with the id {widget.id}')
        #         self.connectionsID.remove(widget.id)
        #         widget.deleteLater()
        #         self.shortcutHandle.remove_shortcut(widget.shortcut)




                

app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec())

















# 08/04/2023 15:47
            # self._connected_servers.append((serverIP, serverPort))
        # self._client = Client(serverIP, serverPort)
        # self._clientSignals = ClientSignals(self._client.recived_messages)
        # self._threabool.start(self._client)
        # self._threabool.start(self._clientSignals)
        # if(self.serverWidgets[id-1].connectButton.isChecked()):
        #     self.serverWidgets[id-1].connectButton.change_style_on_checked(True)
        #     self.reciveMouseMovementWorkers.append(ReciveUserInput(serverIP, serverPort, id))
        #     self.reciveMouseMovementWorkers[-1].signal.serverStoped.connect(self._remove_server_widget)
        #     self.threabool.start(self.reciveMouseMovementWorkers[-1])
        # else:
        #     self.serverWidgets[id-1].connectButton.change_style_on_checked(False)
        #     for worker in self.reciveMouseMovementWorkers:
        #         if (worker.id == id):
        #             worker.alive = False
        # if (serverIP, serverPort) in self._connected_servers:
        #     print(f'\nmainwindow, _connect_to_server, server:{serverIP}:{serverPort} allready exist' \
        #           '\nchecking if client is connected/disonnected')
        #     if self._client.is_connected():
        #         print('\nmainwindow, _connect_to_server, client connected - > closing the connection')
        #         self._client.close_connection()
        #         print('\nmainwindow, _connect_to_server, connection CLOSED|||')
        #     else:
        #         self._client.re_open_connection()
        #         print('\nmainwindow, _connect_to_server, connection RESUMMED>>>')
        #     return
#region _client_view_add_server
        # self._clientViewWidgets.append(ServerWidget(serverName, serverIP, serverPort))
        # self.clientView.scrollArea.add_device(self._clientViewWidgets[-1])
        # self._clientViewWidgets[-1].connectButton.clicked.connect(lambda: self._connect_to_server(serverIP, serverPort))
#endregion
#now we know that there is a socket on this ip address and this pre-defined port
# we knew that because we could ping this ip address:port
# we did not estaplish any TCP connections to this socket port
#on the SERVER side nothing happened yet.
#we create a server widget for this socket
# this widget has a [connect button]
########################################################
#when we press the connection button ->
# create a client instance
# connectet to the server
# change the connection button style
#When we press again ->
# we want to close the connection
# change the button style
#when we press the connection button ->
# connectet to the server
# change the connection button style