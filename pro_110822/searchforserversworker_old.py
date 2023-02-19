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
    infoSignal = Signal(object, object)

class SearchForServersWorker(QRunnable):
    def __init__(self, port: int)-> None:
        super().__init__()
        self.signal = SearchForServersWorkerSignals()
        self.serverPort = port


    @Slot()
    def run(self)-> int:
        searchForServerConnection = MouseAndKeyboardConnection()
        searchForServerConnection.create_socket(180)
        scan = NetWrokScanner()

        self.signal.infoSignal.emit(10, 'Searching for servers...')
        devicesList = scan.get_local_addresses_from_arp()
        devicesName = scan.get_connected_devices_name()


        self.signal.infoSignal.emit(15, ('Found ' + str(len(devicesList)) + ' device/s'))
        time.sleep(1)
        if (len(devicesList) == 0):
            self.signal.infoSignal.emit(15, 'No servers found!')
            time.sleep(2)
            self.signal.infoSignal.emit(0, ' ')
            return
        else:
            initProgressValue = 85/len(devicesList)
            progressValue = initProgressValue


        for device_IP in devicesList:

            self.signal.infoSignal.emit(progressValue, ('Trying ' + device_IP + ':' + str(self.serverPort)))
            if(searchForServerConnection.connect_to_server(device_IP, self.serverPort)):
                self.signal.infoSignal.emit(999, (device_IP + ':' + str(self.serverPort) +' connection OK!.'))
                found = False
                for name in devicesName:
                    if device_IP in name[2]:
                        self.signal.foundServer.emit(name[0], device_IP, self.serverPort)
                        found = True
                if (not found):
                    self.signal.foundServer.emit("Unknown", device_IP, self.serverPort)

            else:
                self.signal.infoSignal.emit(999, (device_IP + ':' + str(self.serverPort) +' connection refused!.'))
            progressValue = progressValue + initProgressValue


        searchForServerConnection.terminate_socket()
        self.signal.infoSignal.emit(100, 'No servers found!')
        time.sleep(2)
        self.signal.infoSignal.emit(0, ' ')



        return(1)
