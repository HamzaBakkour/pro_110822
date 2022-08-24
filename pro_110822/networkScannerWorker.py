from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from networkScanner import get_connected_devices_name
from connection import mouseAndKeyboardConnection
from time import sleep


class searchForServersWorkerSignals(QObject):
    sendSignal = Signal(list)

class searchForServersWorker(QRunnable):
    def __init__(self, port: int)-> None:
        super(searchForServersWorker, self).__init__()
        self.signal = searchForServersWorkerSignals()
        self.searchConnection = mouseAndKeyboardConnection()
        self.searchConnection.createSocket(2)
        self.serverPort = port
    
    @Slot()
    def run(self)-> int:
        devicesList = get_connected_devices_name()
        serverFound = False
        for device in devicesList:
            try:
                self.searchConnection.connectToServer(device[2][0], self.serverPort)
                serverFound = True
            except OSError:
                print("OSError in networkScannerWorker")
                pass
            if (serverFound):
                self.signal.sendSignal.emit(device)
                serverFound = False
        self.searchConnection.terminateSocket()
        print("searchForServersWorker socket terminated")
        return(1)