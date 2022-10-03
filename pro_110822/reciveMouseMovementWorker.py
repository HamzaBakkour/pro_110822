from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from socketconnection import MouseAndKeyboardConnection
import socket

import sys
import os
import traceback
import logging
import time
import re

class ReciveMouseMovementWorkerSignals(QObject):
    updateSignal = Signal(object)

class ReciveMouseMovementWorker(QRunnable):
    def __init__(self, serverIP: str, serverPort: str)-> None:
        super(ReciveMouseMovementWorker, self).__init__()
        self.serverIP = serverIP
        self.serverPort = int(serverPort)


    @Slot()
    def run(self)-> int:
        clientSocket = socket.socket()
        clientSocket.connect((self.serverIP, self.serverPort)) 
        message = " " 
        while message.lower().strip() != 'bye':
            data = clientSocket.recv(1024).decode()  
            print('Received from server: ' + data)  
        clientSocket.close()
