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
        self.serverSocket = socket.socket()
        self.serverInfoToClientSocket = socket.socket()
        self.serverSocket.bind(('', self.serverPort))
        self.serverInfoToClientSocket.bind(('', 12346))

        while (self.terminate == False):
            print("server is listning for connections")
            self.serverSocket.listen(5)
            try:
                conn, address = self.serverSocket.accept()
                print("Connection from: " + str(address))
            except:
                pass
            
            while (self.terminate == False):
                self.serverInfoToClientSocket.listen(60)
                try:
                    connS, addressS = self.serverInfoToClientSocket.accept()
                    self.signal.createSocket.emit(addressS, "12348")
                    #This data tells the client which port to use to recive mouse movement
                    data = "12348"
                    connS.send(data.encode())  
                except:
                    print("**INFO** listenforconnectionsworker.py ListenForConnectionsWorker run [2]")
                    


            print("breaked")