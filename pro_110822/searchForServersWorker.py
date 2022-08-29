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
    pbarSignal = Signal(object, object)

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

        try:
            self.progressValue = 85/len(self.devicesList)
            self.signal.pbarSignal.emit(0, ('Found ' + str(len(self.devicesList)) + ' device/s'))
        except ZeroDivisionError:
            print("searchForServersWorkerSignals, self.devicesList is zero, self.progressValue = 85/len(self.devicesList)")
            exit(0)

        connectionOK = False
        for device in self.devicesList:
            try:
                self.signal.pbarSignal.emit(self.progressValue, ('Trying ' + device))
                self.searchForServerConnection.connectToServer(device, self.serverPort)
                connectionOK = True
            except ConnectionRefusedError:
                part1 = str(sys.exc_info())
                part2 = traceback.format_exc()
                origin = re.search(r'File(.*?)\,', part2).group(1) 
                loggMessage = origin + '\n' + part1  + '\n' + part2
                logging.info(loggMessage)
            if (connectionOK):
                self.signal.pbarSignal.emit(0, (device + ' connection OK!.'))
                self.signal.sendSignal.emit(device)
                connectionOK = False
        self.searchForServerConnection.terminateSocket()
        self.signal.pbarSignal.emit(999, ' ')


        return(1)