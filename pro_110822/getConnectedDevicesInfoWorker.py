from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from networkScannerCls import netWrokScanner

import sys
import traceback
import logging
import re

import pdb

class getConnectedDevicesInfoWorkerSignals(QObject):
    sendSignal = Signal(object)

class getConnectedDevicesInfoWorker(QRunnable):
    def __init__(self)-> None:
        super(getConnectedDevicesInfoWorker, self).__init__()
        self.signal = getConnectedDevicesInfoWorkerSignals()
        self.searchForDevices = netWrokScanner()
        
        
    
    @Slot()
    def run(self)-> int:
        print("Searching for devices.")
        devicesList = ""

        try:
            devicesList = self.searchForDevices.get_connected_devices_name()
        except ConnectionRefusedError:
            part1 = str(sys.exc_info())
            part2 = traceback.format_exc()
            origin = re.search(r'File(.*?)\,', part2).group(1) 
            loggMessage = origin + '\n' + part1  + '\n' + part2
            logging.info(loggMessage)
        
        self.signal.sendSignal.emit(devicesList)
        print("Searching for devices ended.")
        return(1)