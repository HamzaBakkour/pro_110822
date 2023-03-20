from PySide6.QtCore import QRunnable, QObject, Signal, Slot
import os
import inspect
import time
import socket



class ConnectionsMonitorSignals(QObject):
    socketError = Signal(object)

class ConnectionsMonitor(QRunnable):
    def __init__(self, connectionsList : list[dict[str, socket.socket]])-> None:
        super(ConnectionsMonitor, self).__init__()
        self.alive = True
        self.connectionsList = connectionsList
        self._signal = ConnectionsMonitorSignals()
        self._port = None

    def _emmit_signal(self, signal):
        self._signal.socketError.emit(signal)

    def _send_test_message(self, connection):
        connection.sendall('*'.encode())

    def _get_port(self, connection) -> int:
        return connection.getsockname()[1]
    
    def _close_connection(self, connection):
        try:
            connection.close()
        except socket.error as error:
            if(error.errno == 10038):
                print(f'{os.path.basename(__file__)} | ',
                      f'{inspect.stack()[0][3]} | ',
                      'Exception raside : [OK]')
            else:
                print(f'{os.path.basename(__file__)} |',
                      f'{inspect.stack()[0][3]} | ',
                      f'Exception raside, errorno : {error.errno} [-]')
        except Exception as ex:
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'Exception raside : {ex} [Unhandeled]')


    def _remove_connection(self, connection):
        try:
            self.connectionsList.remove(connection)
        except ValueError as ve:
            print(f'{os.path.basename(__file__)} | ',
                  f'{inspect.stack()[0][3]} | ',
                  f'Value error [OK]: {ve}')

    @Slot()
    def run(self)-> None:
        while(self.alive):
            for connection in self.connectionsList:
                try:
                    self._send_test_message(connection['connection']) # type: ignore
                except socket.error:
                    self._port = self._get_port(connection['connection']) # type: ignore
                    self._emmit_signal(self._port)
                    self._close_connection(connection['connection']) # type: ignore
                    self._remove_connection(connection)
                    time.sleep(1)
                except StopIteration:
                    pass
                except Exception as e:
                    raise OSError(f'{os.path.basename(__file__)} | ',
                                  f'{inspect.stack()[0][3]} | ', 
                                  str(e),
                                  '\n',
                                  type(e))
            time.sleep(0.5)
        print(f'{os.path.basename(__file__)} | ',
              f'{inspect.stack()[0][3]} | ',
              'ConnectionsMonitor terminated')
        
