from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from socketconnection import MouseAndKeyboardConnection
from networkscannercls import NetWrokScanner

import sys
import os
import traceback
import logging
import time
import re

import pdb
# pdb.set_trace()
class SearchForServersWorkerSignals(QObject):
    foundServer = Signal(object, object, object)
    pbarSignal = Signal(object, object)

class SearchForServersWorker(QRunnable):
    def __init__(self, port: int)-> None:
        
        super(SearchForServersWorker, self).__init__()
        self.signal = SearchForServersWorkerSignals()
        self.searchForServerConnection = MouseAndKeyboardConnection()
        self.searchForServerConnection.create_socket(5)
        self.serverPort = port
        self.scan = NetWrokScanner()

    @Slot()
    def run(self)-> int:
        # pdb.set_trace()
        devicesList = self.scan.get_local_addresses_from_arp()
        devicesName = self.scan.get_connected_devices_name()

        try:
            self.signal.pbarSignal.emit(0, ('Found ' + str(len(devicesList)) + ' device/s'))
            self.progressValue = 85/len(devicesList)
        except ZeroDivisionError:
            part1 = str(sys.exc_info())
            part2 = traceback.format_exc()
            origin = re.search(r'File(.*?)\,', part2).group(1) 
            loggMessage = origin + '\n' + part1  + '\n' + part2
            logging.info(loggMessage)
            exit(-1)

        for device_IP in devicesList:
            try:
                self.signal.pbarSignal.emit(self.progressValue, ('Trying ' + device_IP + ':' + str(self.serverPort)))
                if(self.searchForServerConnection.connect_to_server(device_IP, self.serverPort)):
                    self.signal.pbarSignal.emit(0, (device_IP + ':' + str(self.serverPort) +' connection OK!.'))
                    found = False
                    for name in devicesName:
                        if device_IP in name[2]:
                            self.signal.foundServer.emit(name[0], device_IP, self.serverPort)
                            found = True
                    if (not found):
                        self.signal.foundServer.emit("Unknown", device_IP, self.serverPort)

                else:
                    self.signal.pbarSignal.emit(0, (device_IP + ':' + str(self.serverPort) +' connection refused!.'))
            except :
                part1 = str(sys.exc_info())
                part2 = traceback.format_exc()
                origin = re.search(r'File(.*?)\,', part2).group(1) 
                loggMessage = origin + '\n' + part1  + '\n' + part2
                logging.info(loggMessage)

        self.searchForServerConnection.terminate_socket()
        self.signal.pbarSignal.emit(999, ' ')


        return(1)