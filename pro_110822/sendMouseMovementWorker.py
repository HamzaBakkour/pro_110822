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

class sendMouseMovementWorkerSignals(QObject):
    updateSignal = Signal(object)

class sendMouseMovementWorker(QRunnable):
    def __init__(self, clientIP: str)-> None:
        super(sendMouseMovementWorker, self).__init__()
        self.clientIP = clientIP
        self.connection = mouseAndKeyboardConnection()
        

    def initConnection(self):
        self.connection.createSocket(None)

    def acceptConnectionFromClient(self):
        self.connection.acceptClientConnection(self.serverIP)

    @Slot()
    def run(self)-> int:
        self.initConnection()
        self. acceptConnectionFromClient()
        self.connection.sendMouseMovement()
