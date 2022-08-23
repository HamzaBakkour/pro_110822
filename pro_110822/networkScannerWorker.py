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
        self.searchConnection.initSocket(2)
        self.serverPort = port
    
    @Slot()
    def run(self)-> int:
        devicesList = get_connected_devices_name()
        serverFound = False
        for device in devicesList:
            print("Trying to connect ot {} with IP {}".format(device[0], device[1]))
            try:
                self.searchConnection.connectToServer(device[1], self.serverPort)
                serverFound = True
            except:
                print("searhcForServersWorker connectToServer exceotion occured")
                pass
            if (serverFound):
                self.signal.sendSignal.emit(device)
                serverFound = False
        return(1)




