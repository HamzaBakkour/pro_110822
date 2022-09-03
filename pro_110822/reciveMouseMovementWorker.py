from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from socketConnection import mouseAndKeyboardConnection
import socket

import sys
import os
import traceback
import logging
import time
import re

# import pdb
class reciveMouseMovementWorkerSignals(QObject):
    updateSignal = Signal(object)

class reciveMouseMovementWorker(QRunnable):
    def __init__(self, serverIP: str, serverPort: int)-> None:
        super(reciveMouseMovementWorker, self).__init__()
        self.serverIP = serverIP
        self.serverPort = serverPort


    @Slot()
    def run(self)-> int:
        s = socket.socket()
        s.connect((self.serverIP, self.serverPort))
        print("recived : ")
        print (s.recv(1024).decode())
        s.close()



