from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from socketconnection import MouseAndKeyboardConnection
import socket

import sys
import os
import traceback
import logging
import time
import re

# import pdb

class SendMouseMovementWorkerSignals(QObject):
    updateSignal = Signal(object)

class SendMouseMovementWorker(QRunnable):
    def __init__(self, clientIP: str)-> None:
        super(SendMouseMovementWorker, self).__init__()
        self.clientIP = clientIP
        self.connection = MouseAndKeyboardConnection()
        

    def init_connection(self):
        self.connection.create_socket(None)

    def accept_connection_from_client(self):
        self.connection.accept_client_connection(self.serverIP)

    @Slot()
    def run(self)-> int:
        self.init_connection()
        self. accept_connection_from_client()
        self.connection.send_mouse_movement()
