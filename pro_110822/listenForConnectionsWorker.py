# from PySide6.QtCore import *
from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from socketConnection import mouseAndKeyboardConnection

import sys
import os
import traceback
import logging
import time
import re

import socket
import datetime

import pdb

class serverWorkerSignals(QObject):
    recivedConnection = Signal(object)

class listenForConnectionsWorker(QRunnable):
    def __init__(self, port: int)-> None:
        super(listenForConnectionsWorker, self).__init__()
        self.serverPort = port
        self.terminate = False

        self.signal = serverWorkerSignals()


    @Slot()
    def run(self)-> int:
        host = socket.gethostname()
        port = 12345

        server_socket = socket.socket()
        sendMovementSocket = socket.socket()

        server_socket.bind((host, port))
        sendMovementSocket.bind((host, 12346))

        while(True):
            print("Started")
            server_socket.listen(1)
            conn, address = server_socket.accept()  
            print("Connection from: " + str(address))
            while True:
                sendMovementSocket.listen(60)
                connS, addressS = sendMovementSocket.accept()  
                print("Waiting for data")
                data = connS.recv(1024).decode()
                if not data:
                    break
                print("from connected user: " + str(data))
                data = input(' -> ')
                connS.send(data.encode())  
            print("breaked")
        conn.close() 