from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from pynput.mouse import Listener, Controller
import socket

import sys
import os
import ctypes
import struct
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

    def get_screen_resulotion(self):
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return screensize

    @Slot()
    def run(self)-> int:
        sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        reciveSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        reciveSocket.bind(('',0))



        sendSocket.connect((self.serverIP, self.serverPort))

        screenRez = self.get_screen_resulotion()
        receiveSocetPort = reciveSocket.getsockname()[1]

        message = "C!{}!{}!{}".format(screenRez[0], screenRez[1], receiveSocetPort)
        message = message.encode()
        header = struct.pack('<L', len(message))

        try:
            sendSocket.sendall(header + message)
        except Exception as e:
            print("***3948pfkro57620***")
            print(str(e))

        reciveSocket.listen(5)
        conn, address = reciveSocket.accept()
        print("from receive worker accepted {} {}".format(conn, address))

        # message = message.encode()
        # header = struct.pack('<L', len(message))
        # try:
        #     clientSocket.sendall(header + message)
        # except Exception as e:
        #     print("***3948pfkro57620***")
        #     print(str(e))

        # clientSocket = socket.socket()
        # clientSocket.connect((self.serverIP, self.serverPort))
        # print("connected to server at ", self.serverIP, ":" ,self.serverPort)

        # mouse = Controller()
        # print("Reciving mouse movement")
        # while (True):
        #     data = clientSocket.recv(1024).decode()
        #     print(data)
        #     if (data == 'TERMINATE'):
        #         clientSocket.shutdown(socket.SHUT_RDWR)
        #         clientSocket.close()
        #         return(0)
        #     if (data != ''):
        #         try:
        #             x = re.search('aa(.*?)bb',data).group(1)
        #             y = re.search('bb(.*?)cc',data).group(1)
        #         except AttributeError:#invaild data will casuse AttributeError
        #             part1 = str(sys.exc_info())
        #             part2 = traceback.format_exc()
        #             origin = re.search(r'File(.*?)\,', part2).group(1) 
        #             loggMessage = origin + '\n' + part1  + '\n' + part2
        #             logging.info(loggMessage)
        #             continue
        #     else:
        #         continue
        #     x = int(x)
        #     y = int(y)
        #     print("x:", x, "y:", y)
        #     mouse.position = (x, y)



        # clientSocket.close()
