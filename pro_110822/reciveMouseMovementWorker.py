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
    def __init__(self, serverIP: str, serverPort: int)-> None:
        super(ReciveMouseMovementWorker, self).__init__()
        self.serverIP = serverIP
        self.serverPort = serverPort


    @Slot()
    def run(self)-> int:
        port = 12346

        clientSocket = socket.socket() 
        clientSocket.connect(('192.168.0.5', port)) 
        message = input(" -> ") 
        while message.lower().strip() != 'bye':
            clientSocket.send(message.encode())  
            data = clientSocket.recv(1024).decode()  
            print('Received from server: ' + data)  
            message = input(" -> ")  
        clientSocket.close()  




