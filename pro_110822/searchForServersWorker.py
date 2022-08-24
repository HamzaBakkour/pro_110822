from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from networkScanner import get_connected_devices_name
from socketConnection import mouseAndKeyboardConnection

import sys
import os
import traceback
import logging
import time
import re


# logging.basicConfig(filename=(time.strftime("%Y%m%d-%H%M%S") + os.path.basename(__file__) + '.txt'), level=logging.DEBUG,
# format="%(levelname)s\n%(asctime)s\n%(message)s", filemode="w")

class searchForServersWorkerSignals(QObject):
    sendSignal = Signal(list)

class searchForServersWorker(QRunnable):
    def __init__(self, port: int)-> None:
        super(searchForServersWorker, self).__init__()
        self.signal = searchForServersWorkerSignals()
        self.searchConnection = mouseAndKeyboardConnection()
        self.searchConnection.createSocket(None)
        self.serverPort = port
    
    @Slot()
    def run(self)-> int:
        devicesList = get_connected_devices_name()
        serverFound = False
        for device in devicesList:
            try:
                # print("search for server worker trying to connect to {} at ip {} and port {}".format(device[0] , device[2][0], self.serverPort))
                self.searchConnection.connectToServer(device[2][0], self.serverPort)
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
        self.searchConnection.terminateSocket()
        print("searchForServersWorker socket terminated")
        return(1)