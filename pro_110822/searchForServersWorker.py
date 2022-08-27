from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from socketConnection import mouseAndKeyboardConnection
from networkScannerCls import netWrokScanner

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
        scan = netWrokScanner()
        self.devicesList = scan.get_local_address_from_arp()
    
    @Slot()
    def run(self)-> int:
        print("Searching for servers.")
        serverFound = False
        for device in self.devicesList:
            try:
                self.searchForServerConnection.connectToServer(device, self.serverPort)
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

        print("Searching for servers ended.")
        return(1)