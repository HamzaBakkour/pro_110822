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
    connectionOkSignal = Signal(object, object)
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
            part1 = str(sys.exc_info())
            part2 = traceback.format_exc()
            origin = re.search(r'File(.*?)\,', part2).group(1) 
            loggMessage = origin + '\n' + part1  + '\n' + part2
            logging.info(loggMessage)
            exit(-1)

        for device in self.devicesList:
            try:
                self.signal.pbarSignal.emit(self.progressValue, ('Trying ' + device + ':' + str(self.serverPort)))
                if(self.searchForServerConnection.connectToServer(device, self.serverPort)):
                    self.signal.pbarSignal.emit(0, (device + ':' + str(self.serverPort) +' connection OK!.'))
                    self.signal.connectionOkSignal.emit(device, self.serverPort)
                else:
                    self.signal.pbarSignal.emit(0, (device + ':' + str(self.serverPort) +' connection refused!.'))
            except :
                part1 = str(sys.exc_info())
                part2 = traceback.format_exc()
                origin = re.search(r'File(.*?)\,', part2).group(1) 
                loggMessage = origin + '\n' + part1  + '\n' + part2
                logging.info(loggMessage)

        self.searchForServerConnection.terminateSocket()
        self.signal.pbarSignal.emit(999, ' ')


        return(1)