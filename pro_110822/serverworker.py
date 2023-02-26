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
import inspect

import pdb

class ServerWorkerSignals(QObject):
    clientRequest = Signal(object)

class ServerWorker(QRunnable):
    def __init__(self, listningSocket : socket.socket)-> None:
        super(ServerWorker, self).__init__()

        self.workerSocket = listningSocket
        self.signal = ServerWorkerSignals()
        self.conn = socket.socket()
        self.alive = True

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
        while (self.alive):
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
                            

                        self.signal.clientRequest.emit(data)
                    else:
                        print("Header data value is not equal to received data length")
            except UnboundLocalError:
                pass
            except BlockingIOError:
                pass
            except IOError:
                pass
            except Exception as ex:
                print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f"Exception rasied:\n{ex}")

        print(f'[*]{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', "ServerWorker terminated")