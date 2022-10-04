from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from pynput.mouse import Listener, Controller
import socket

import sys
import os
import traceback
import logging
import time
import re

import pdb

class SendMouseMovementWorkerSignals(QObject):
    updateSignal = Signal(object)

class SendMouseMovementWorker(QRunnable):
    def __init__(self, clientIP: str, socketPort : str)-> None:
        super(SendMouseMovementWorker, self).__init__()
        print("SendMouseMovementWorker started")
        self.clientIP = clientIP
        self.socketPort = int(socketPort)
        print("clientIP", self.clientIP)
        print("socketPort", self.socketPort)
        

    # def on_move(self, x, y):
    #     print("sending ", x, " ",y)
    #     self.serverSocket.send('aa{}bb{}cc'.format(x, y).encode())

    # def on_click(self, x, y, button, pressed):
    #     print('{} {}'.format(button, 'Pressed' if pressed else 'Released'))

    # def on_scroll(self, x, y, dx, dy):
    #     print('({}, {})'.format(dx, dy))

    

    @Slot()
    def run(self)-> int:
        serverSocket = socket.socket()
        host = socket.gethostname()
        serverSocket.bind((host, self.socketPort))
        serverSocket.listen()
        connS, addressS = serverSocket.accept()
        print("Connection from: XXX" + str(addressS) + "accepted")
        
        mouse = Controller()
        while(True):
            print('{0}'.format(mouse.position))
            # pdb.set_trace()
            connS.send('aa{}bb{}cc'.format(str(mouse.position[0]), str(mouse.position[1])).encode())