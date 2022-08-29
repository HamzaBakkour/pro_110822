# from PySide6.QtCore import *
from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from socketConnection import mouseAndKeyboardConnection

import sys
import os
import traceback
import logging
import time
import re




class serverWorkerSignals(QObject):
    recivedConnection = Signal(object, object)

class listenForConnectionsWorker(QRunnable):
    def __init__(self, port: int)-> None:
        super(listenForConnectionsWorker, self).__init__()
        self.serverPort = port
        self.signal = serverWorkerSignals()
        self.serverConnection = mouseAndKeyboardConnection()
        self.serverConnection.createSocket(5)
        self.terminate = False
        print("Server created.")

    @Slot()
    def run(self)-> int:
        print("Server listning for connection")
        self.serverConnection.listenForConnections(self.serverPort)
        while(self.terminate == False):
            try:
                seocketConnection, addr = self.serverConnection.acceptConnections()
                self.signal.recivedConnection.emit(seocketConnection, addr)
            except TimeoutError: #Tryed to send data on something that is not a socket
                # part1 = str(sys.exc_info())
                # part2 = traceback.format_exc()
                # origin = re.search(r'File(.*?)\,', part2).group(1) 
                # loggMessage = origin + '\n' + part1  + '\n' + part2
                # logging.info(loggMessage)
                pass
        
        self.serverConnection.terminateSocket()
        print("Server terminated")
        return(1)