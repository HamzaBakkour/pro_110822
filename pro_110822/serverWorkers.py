# from PySide6.QtCore import *
from PySide6.QtCore import QRunnable, QObject, Signal, Slot

from connection import mouseAndKeyboardConnection

from time import sleep

class serverWorkerSignals(QObject):
    sendSignal = Signal(object, object)

class listenForConnectionsWorker(QRunnable):
    def __init__(self, port: int)-> None:
        super(listenForConnectionsWorker, self).__init__()
        self.serverPort = port
        self.signal = serverWorkerSignals()
        self.serverConnection = mouseAndKeyboardConnection()

    @Slot()
    def run(self)-> int:
        
        self.serverConnection.listenForConnections(self.serverPort)
        while(True):
            try:
                seocketConnection, addr = self.serverConnection.acceptConnections()
                self.signal.sendSignal.emit(seocketConnection, addr)
            except OSError: #Tryed to send data on something that is not a socket
                print("Exception occured")
                return (-9)

