# from PySide6.QtCore import *
from PySide6.QtCore import QRunnable, QObject, Signal, Slot


import sys
import os
import traceback
import logging
import time
import re

import socket
import datetime

import pdb

class ListningForRequestsWorkerSignals(QObject):
    dataFromClient = Signal(object)

class ListningForRequstsWorker(QRunnable):
    def __init__(self, *listningSocket : socket.socket)-> None:
        super(ListningForRequstsWorker, self).__init__()

        self.workerSocket = listningSocket[0]
        self.signal = ListningForRequestsWorkerSignals()


    @Slot()
    def run(self)-> int:

        print("\nServer is waiting for requsts at port 12345")
        while (True):
            
            # try:
            # data = self.workerSocket.recv(1024).decode()
            # self.signal.dataFromClient.emit(data)
            # print("Recived the following request from client " + data)
            # except:
            #     time.sleep(1)
            time.sleep(60)
            pass
        

            # print("breaked222222")