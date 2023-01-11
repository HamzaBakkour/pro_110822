# from PySide6.QtCore import *
from PySide6.QtCore import QRunnable, QObject, Signal, Slot

import sys
import os
import inspect
import traceback
import logging
import time
import re

import socket
import struct
import datetime

import pdb

class ConnectionsMonitorSignals(QObject):
    socketError = Signal(object)

class ConnectionsMonitor(QRunnable):
    def __init__(self, connectionsList : list[socket.socket])-> None:
        super(ConnectionsMonitor, self).__init__()
        self.alive = True
        self.connectionsList = connectionsList
        self.signal = ConnectionsMonitorSignals()

    @Slot()
    def run(self)-> None:
        while(self.alive):
            for connection in self.connectionsList:
                try:
                    connection.sendall('*'.encode())
                except socket.error as error:
                    # print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'socket error, errno: {error}')
                    try:
                        self.signal.socketError.emit(connection.getsockname()[1])
                        connection.close()
                    except Exception as ex:
                        # print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'Exception raside : {ex}')
                        pass
                    # try:
                    #     self.connectionsList.remove(connection)
                    # except ValueError as ve:
                    #     print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', 'Value error [OK]: {ve}')
                time.sleep(1)
            time.sleep(1)
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', 'ConnectionsMonitor terminated')
        
