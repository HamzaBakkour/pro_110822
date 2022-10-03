from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from pynput.mouse import Listener, Controller
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
        print("connected to server at ", self.serverIP, ":" ,self.serverPort)

        mouse = Controller()
        print("Reciving mouse movement")
        time.sleep(5)
        while (True):
            data = clientSocket.recv(1024).decode()
            print(data)
            if (data == 'TERMINATE'):
                clientSocket.shutdown(socket.SHUT_RDWR)
                clientSocket.close()
                return(0)
            if (data != ''):
                try:
                    x = re.search('aa(.*?)bb',data).group(1)
                    y = re.search('bb(.*?)cc',data).group(1)
                except AttributeError:#invaild data will casuse AttributeError
                    part1 = str(sys.exc_info())
                    part2 = traceback.format_exc()
                    origin = re.search(r'File(.*?)\,', part2).group(1) 
                    loggMessage = origin + '\n' + part1  + '\n' + part2
                    logging.info(loggMessage)
                    continue
            else:
                continue
            x = int(x)
            y = int(y)
            print("x:", x, "y:", y)
            mouse.position = (x, y)



        clientSocket.close()
