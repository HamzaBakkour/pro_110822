from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from socketConnection import mouseAndKeyboardConnection
import socket

import sys
import os
import traceback
import logging
import time
import re

import pdb
# pdb.set_trace()
class reciveMouseMovementWorkerSignals(QObject):
    updateSignal = Signal(object)

class reciveMouseMovementWorker(QRunnable):
    def __init__(self, serverIP: str, serverPort: int)-> None:
        super(reciveMouseMovementWorker, self).__init__()
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.connection = mouseAndKeyboardConnection()
        

    def initConnection(self):
        self.connection.createSocket(None)
        self.connection.connectToServer(self.serverIP, self.serverPort)
        pass


    @Slot()
    def run(self)-> int:
        self.initConnection()
        self.connection.reciveMouseMovement()