# from PySide6.QtCore import *
from email import header
from errno import WSAEWOULDBLOCK
from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from socketconnection import MouseAndKeyboardConnection

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
            print("1")
            self.workerSocket.listen(5)
            print("2")
            try:
                print("3")
                self.conn, address = self.workerSocket.accept()
                print("4")
                print("Client at {} searching for server".format(str(address)))
                print("5")
                self.signal.connectionFromClient.emit(address)
                print("6")
            except Exception as e:#BlockingIOError
                print("7")
                print(str(e))
                print("8")
                time.sleep(1)

            try:
                print("9")
                headerData = self.receive_n_bytes(4)
                print("10")
                if (len(headerData) == 4):
                    print("11")
                    messageLen = struct.unpack('<L', headerData)[0]
                    print("12")
                    data = self.receive_n_bytes(messageLen)
                    print("13")
                    if len(data) == messageLen:
                        print("14")
                        print(data.decode())
                        print("15")
            except Exception as e :#UnboundLocalError
                print(str(e))
            except BlockingIOError:
                pass
            except IOError:
                pass
            print("16")
        print("out")