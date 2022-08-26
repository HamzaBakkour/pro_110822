from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from networkScanner import get_connected_devices_name
from socketConnection import mouseAndKeyboardConnection

import sys
import os
import traceback
import logging
import time
import re

import pdb

class searchForServersWorkerSignals(QObject):
    sendSignal = Signal(object)

class searchForServersWorker(QRunnable):
    def __init__(self, port: int)-> None:
        super(searchForServersWorker, self).__init__()
        self.signal = searchForServersWorkerSignals()
        self.searchForServerConnection = mouseAndKeyboardConnection()
        self.searchForServerConnection.createSocket(5)
        self.serverPort = port
        self.devicesList = get_connected_devices_name()
    
    @Slot()
    def run(self)-> int:
        # pdb.set_trace()
        
        serverFound = False
        for device in self.devicesList:
            try:
                # print("search for server worker trying to connect to {} at ip {} and port {}".format(device[0] , device[2][0], self.serverPort))
                self.searchForServerConnection.connectToServer(device[2][0], self.serverPort)
                serverFound = True
            except ConnectionRefusedError:
                part1 = str(sys.exc_info())
                part2 = traceback.format_exc()
                origin = re.search(r'File(.*?)\,', part2).group(1) 
                loggMessage = origin + '\n' + part1  + '\n' + part2
                logging.info(loggMessage)
            if (serverFound):
                self.signal.sendSignal.emit(device)
                serverFound = False
        self.searchForServerConnection.terminateSocket()

        print("searchForServersWorker socket terminatedxx")
        return(1)