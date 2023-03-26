from PySide6.QtCore import QThreadPool,QRunnable, Slot
import time
from asyncClientTest import AsyncClient


class Client(QRunnable):
    def __init__(self) -> None:
        super(Client, self).__init__()
        self._client = AsyncClient()
        self.serverIP = None
        self.serverPort = None


    def connect(self, serverIP, serverPort):
        self.serverIP = serverIP
        self.serverPort = serverPort

    def _connect(self):
        self._client.connect(self.serverIP, self.serverPort )
        

    def send_data(self, data):
        self._client.send_data(data)


    def recived_messages(self):
        return self._client.recived_messages()
    
    def close_connection(self):
        self._client.close_connection()

    @Slot()
    def run(self)-> None:
        self._connect()



def wait(sec):
    while (sec > 0):
        print(f"waiting {sec}s")
        time.sleep(1)
        sec = sec -1




client = Client()
client.connect('127.0.0.1', 8888)

threabool = QThreadPool()
threabool.setMaxThreadCount(25)
threabool.start(client)

client.send_data('hello from client2')

client.close_connection()

wait(1)

recived_messages = client.recived_messages()

wait(1)
