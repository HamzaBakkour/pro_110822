# from PySide6.QtCore import *
from PySide6.QtCore import QRunnable, QObject, Signal, Slot

from socketConnection import mouseAndKeyboardConnection

import sys
import os
import traceback
import logging
import time
import re


# logging.basicConfig(filename=(time.strftime("%Y%m%d-%H%M%S") + os.path.basename(__file__) + '.txt'), level=logging.DEBUG,
# format="%(levelname)s\n%(asctime)s\n%(message)s", filemode="w")


class serverWorkerSignals(QObject):
    sendSignal = Signal(object, object)

class listenForConnectionsWorker(QRunnable):
    def __init__(self, port: int)-> None:
        super(listenForConnectionsWorker, self).__init__()
        self.serverPort = port
        self.signal = serverWorkerSignals()
        self.serverConnection = mouseAndKeyboardConnection()
        self.serverConnection.createSocket(5)
        self.terminate = False

    @Slot()
    def run(self)-> int:
        self.serverConnection.listenForConnections(self.serverPort)
        while(self.terminate == False):
            try:
                seocketConnection, addr = self.serverConnection.acceptConnections()
                self.signal.sendSignal.emit(seocketConnection, addr)
            except TimeoutError: #Tryed to send data on something that is not a socket
                # part1 = str(sys.exc_info())
                # part2 = traceback.format_exc()
                # origin = re.search(r'File(.*?)\,', part2).group(1) 
                # loggMessage = origin + '\n' + part1  + '\n' + part2
                # logging.info(loggMessage)
                pass
        
        print("listenForConnectionsWorker terminated")
        self.serverConnection.terminateSocket()
        print("listenForConnectionsWorker returned")
        return(1)