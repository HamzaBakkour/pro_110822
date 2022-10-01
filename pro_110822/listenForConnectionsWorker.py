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
    recivedConnection = Signal(object)

class ListenForConnectionsWorker(QRunnable):
    def __init__(self, port: int)-> None:
        super(ListenForConnectionsWorker, self).__init__()
        self.serverPort = port
        self.terminate = False

        self.signal = ServerWorkerSignals()


    @Slot()
    def run(self)-> int:
        host = socket.gethostname()
        port = 12345

        serverSocket = socket.socket()
        sendMovementSocket = socket.socket()

        serverSocket.bind((host, port))
        sendMovementSocket.bind((host, 12346))

        while(True):
            print("Started")
            serverSocket.listen(1)
            conn, address = serverSocket.accept()  
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