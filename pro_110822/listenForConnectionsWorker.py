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

class ListningWorkerSignals(QObject):
    connectionFromClient = Signal(object)

class ListenForConnectionsWorker(QRunnable):
    def __init__(self, listningSocket : socket.socket)-> None:
        super(ListenForConnectionsWorker, self).__init__()

        self.workerSocket = listningSocket
        self.signal = ListningWorkerSignals()

    @Slot()
    def run(self)-> int:

        print("Server is listning for connections at port 12345")
        while (True):
            
            self.workerSocket.listen(1)
            # try:
            conn, address = self.workerSocket.accept()
            print("Client at {} searching for server".format(str(address)))
            self.signal.connectionFromClient.emit(address)
            # except:
                # pass
        

            print("breaked11111111")