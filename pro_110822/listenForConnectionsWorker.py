# from PySide6.QtCore import *
from PySide6.QtCore import QRunnable, QObject, Signal, Slot

import sys
import os
import traceback
import logging
import time
import re

import socket
import struct
import datetime

import pdb

class ListningWorkerSignals(QObject):
    connectionFromClient = Signal(object)

class ListenForConnectionsWorker(QRunnable):
    def __init__(self, listningSocket : socket.socket)-> None:
        super(ListenForConnectionsWorker, self).__init__()

        self.workerSocket = listningSocket
        self.signal = ListningWorkerSignals()
        self.conn = socket.socket()

    def receive_n_bytes(self, n):
        """ Convenience method for receiving exactly n bytes from
            self.socket (assuming it's open and connected).
        """
        data = ''.encode()
        while len(data) < n:
            chunk = self.conn.recv(n - len(data))
            if ((chunk == ''.encode())):
                break
            data += chunk
        return data

    @Slot()
    def run(self)-> int:

        print("Server is listning for connections at port 12345")
        while (True):
            self.workerSocket.listen(5)
            try:
                self.conn, address = self.workerSocket.accept()
                # print("Client at {} searching for server".format(str(address)))
            except BlockingIOError:
                pass
                time.sleep(1)

            try:
                headerData = self.receive_n_bytes(4)
                if (len(headerData) == 4):
                    dataLen = struct.unpack('<L', headerData)[0]
                    data = self.receive_n_bytes(dataLen)
                    if len(data) == dataLen:
                        data = data.decode()

                        if (data.split('!')[0] == 'C'):
                            data = data + '!' + self.conn.getpeername()[0]
                            

                        self.signal.connectionFromClient.emit(data)
                    else:
                        print("Header data value is not equal to received data length")
            except UnboundLocalError:
                pass
            except BlockingIOError:
                pass
            except IOError:
                pass