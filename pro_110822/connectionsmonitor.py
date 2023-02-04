from PySide6.QtCore import QRunnable, QObject, Signal, Slot

import os
import inspect
import time
import socket


class ConnectionsMonitorSignals(QObject):
    socketError = Signal(object)

class ConnectionsMonitor(QRunnable):
    def __init__(self, connectionsList : list[socket.socket])-> None:
        super(ConnectionsMonitor, self).__init__()
        self.alive = True
        self.connectionsList = connectionsList
        self.signal = ConnectionsMonitorSignals()

    @Slot()
    def run(self)-> None:
        while(self.alive):
            for connection in self.connectionsList:
                try:
                    connection[0].sendall('*'.encode())
                except socket.error as error:
                    try:
                        self.signal.socketError.emit(connection[0].getsockname()[1])
                        connection[0].close()
                    except Exception as ex:
                        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'Exception raside : {ex}')
                time.sleep(1)
            time.sleep(1)
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', 'ConnectionsMonitor terminated')
        
