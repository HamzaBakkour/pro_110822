from PySide6.QtCore import QRunnable, QObject
from connection import mouseAndKeyboardConnection

class serverWorkerSignals(QObject):
    sendSignal = pyqtSignal(object, object)

class serverWorker(QRunnable):
    def __init__(self, port: int)-> None:
        super(serverWorker, self).__init__()
        self.serverPort = port
        self.signal = serverWorkerSignals()

    @pyqtSlot()
    def run(self):
        self.serverConnection = mouseAndKeyboardConnection()
        self.serverConnection.listenForConnections()
        while(True):
            seocketConnection, addr = self.serverConnection.acceptConnections()
            self.signal.sendSignal.emit(seocketConnection, addr)