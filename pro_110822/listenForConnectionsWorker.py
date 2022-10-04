# from PySide6.QtCore import *
from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from socketconnection import MouseAndKeyboardConnection

import sys
import os
import traceback
import logging
import time
import re

import socket
import datetime

import pdb

class ServerWorkerSignals(QObject):
    createSocket = Signal(object, object)

class ListenForConnectionsWorker(QRunnable):
    def __init__(self, port: int)-> None:
        super(ListenForConnectionsWorker, self).__init__()
        self.serverPort = port
        self.terminate = False

        self.signal = ServerWorkerSignals()


    @Slot()
    def run(self)-> int:
        host = socket.gethostname()
        serverSocket = socket.socket()
        infoToClientSocket = socket.socket()
        serverSocket.bind((host, self.serverPort))
        infoToClientSocket.bind((host, 12346))

        while(True):
            print("server is listning for connections")
            serverSocket.listen(1)
            conn, address = serverSocket.accept()  
            print("Connection from: " + str(address))
            while True:
                infoToClientSocket.listen(60)
                connS, addressS = infoToClientSocket.accept()
                #This data tells the client which port to use to recive mouse movement
                self.signal.createSocket.emit(addressS, "12348")

                data = "12348"
                connS.send(data.encode())  
            print("breaked")
        conn.close() 