# from PySide6.QtCore import *
from PySide6.QtCore import QRunnable, QObject, Signal, Slot

from connection import mouseAndKeyboardConnection

class serverWorkerSignals(QObject):
    sendSignal = Signal(object, object)

class serverWorker(QRunnable):
    def __init__(self, port: int)-> None:
        super(serverWorker, self).__init__()
        self.serverPort = port
        self.signal = serverWorkerSignals()

    @Slot()
    def run(self):
        self.serverConnection = mouseAndKeyboardConnection()
        self.serverConnection.listenForConnections(self.serverPort)
        while(True):
            seocketConnection, addr = self.serverConnection.acceptConnections()
            self.signal.sendSignal.emit(seocketConnection, addr)