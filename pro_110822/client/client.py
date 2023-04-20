from PySide6.QtCore import QRunnable, Slot, QObject, Signal
from asyncio.exceptions import CancelledError
from client.asyncclient import AsyncClient


# class CSignal(QObject):
#      recived_messages = Signal(object)

# class ClientSignals(QRunnable):
#     def __init__(self, recived_messages) -> None:
#         super(ClientSignals, self).__init__()
#         self.signal = CSignal()
#         self.recived_messages = recived_messages
#         self.alive = True
#         self.tick = 1
#     @Slot()
#     def run(self) -> None:
#         while(self.alive):
#             self.signal.recived_messages.emit(self.recived_messages)
#             time.sleep(self.tick)

class CSignal(QObject):
     remove_server = Signal(object, object)

class Client(QRunnable):
    def __init__(self, serverIP, serverPort) -> None:
        super(Client, self).__init__()
        self._client = AsyncClient()
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.signals = CSignal()
        self.alive = True

    @property
    def recived_messages(self):
        return self._client.recived_messages()
    
    
    def is_connected(self):
        return self._client.is_connected()

    def _connect(self):
        self._client.connect(self.serverIP, self.serverPort )

    def send_data(self, data):
        self._client.send_data(data)

    def close_connection(self):
        self._client.close_connection()


    @Slot()
    def run(self)-> None:
        print('client, run, STARTED')
        try:
            self._connect()
        except CancelledError:
                print('\nclient, run, _connect raised exeption, CancelledError')
                print(f'\nclient, run, _connect raised exeption, EMMITING REMOVE SIGNAL with {self.serverIP}:{self.serverPort} to mainwindow ->')
                self.signals.remove_server.emit(self.serverIP, self.serverPort)
        except Exception as ex:
                print(f'\nclient, run, _connect raised exeption, {type(ex)}, {ex}')
                print(f'\nclient, run, _connect raised exeption, EMMITING REMOVE SIGNAL with {self.serverIP}:{self.serverPort} to mainwindow ->')
                self.signals.remove_server.emit(self.serverIP, self.serverPort)
        print("\nclient, run, 'asyncclient' did not raise exprion -> NOT EMMITING remove server signal")

        print('client, run, ENDED')

   


    # @Slot()
    # def run(self)-> None:
    #     print('client, run, started')
    #     try:
    #         self._connect()
    #     except Exception as ex:
    #         print(f'\nclient, run, _connect raised exeption, {type(ex)}, {ex}')
    #         print(f'\nclient, run, _connect raised exeption, EMMITING REMOVE SIGNAL with {self.serverIP}:{self.serverPort} to mainwindow ->')
    #         self.signals.remove_server.emit(self.serverIP, self.serverPort)
    #     print("\nclient, run, 'asyncclient' did not raise exprion -> NOT EMMITING remove server signal")       


# class CSignal(QObject):
#      recived_messages = Signal(object)

# class ClientSignals(QRunnable):
#     def __init__(self, recived_messages) -> None:
#         super(ClientSignals, self).__init__()
#         self.signal = CSignal()
#         self.recived_messages = recived_messages
#         self.alive = True
#         self.tick = 1
#     @Slot()
#     def run(self) -> None:
#         while(self.alive):
#             self.signal.recived_messages.emit(self.recived_messages)
#             time.sleep(self.tick)


    # def resume_connection(self):
    #     self._client.reopen_connection()

# client = Client()
# client.connect('127.0.0.1', 8888)

# threabool = QThreadPool()
# threabool.setMaxThreadCount(25)
# threabool.start(client)


# client.send_data('hello from client1')

# client.close_connection()

# recived_messages = client.recived_messages()

# print('ended')







# self._inbound_handle_thread = threading.Thread(target=self._handle_inbound_data)     
# self._inbound_handle_thread.start()











    # def connect(self, serverIP, serverPort):
    #     self.serverIP = serverIP
    #     self.serverPort = serverPort