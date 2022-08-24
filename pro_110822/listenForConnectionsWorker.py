# from PySide6.QtCore import *
from PySide6.QtCore import QRunnable, QObject, Signal, Slot

from socketConnection import mouseAndKeyboardConnection

import sys
import traceback

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
                print(sys.exc_info())
                print (traceback.format_exc())
                
        self.serverConnection.terminateSocket()
        return(1)