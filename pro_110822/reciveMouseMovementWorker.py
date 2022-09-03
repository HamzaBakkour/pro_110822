from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from socketConnection import mouseAndKeyboardConnection
import socket

import sys
import os
import traceback
import logging
import time
import re

class reciveMouseMovementWorkerSignals(QObject):
    updateSignal = Signal(object)

class reciveMouseMovementWorker(QRunnable):
    def __init__(self, serverIP: str, serverPort: int)-> None:
        super(reciveMouseMovementWorker, self).__init__()
        self.serverIP = serverIP
        self.serverPort = serverPort


    @Slot()
    def run(self)-> int:
        port = 12346

        client_socket = socket.socket() 
        client_socket.connect(('192.168.0.5', port)) 
        message = input(" -> ") 
        while message.lower().strip() != 'bye':
            client_socket.send(message.encode())  
            data = client_socket.recv(1024).decode()  
            print('Received from server: ' + data)  
            message = input(" -> ")  
        client_socket.close()  




