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
                    connection['connection'].sendall('*'.encode())
                except socket.error as error:
                    print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'socket error, errno: {error}')

                    try:
                        self.signal.socketError.emit(connection['connection'].getsockname()[1])
                        connection['connection'].close()
                    except socket.error as error:
                        if(error.errno == 10038):
                            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'Exception raside : {ex} [OK]')
                    except Exception as ex:
                        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'Exception raside : {ex} [Unhandeled]')
                        pass
                    try:
                        self.connectionsList.remove(connection)
                    except ValueError as ve:
                        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', 'Value error [OK]: {ve}')

                time.sleep(1)
            time.sleep(1)
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', 'ConnectionsMonitor terminated')
        
