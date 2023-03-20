import unittest
from unittest.mock import patch
import socket
from socket import SHUT_RDWR
import time
import threading
from pro_110822.reciveuserinput import ReciveUserInput


class TestReciveuserinput(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.testSocketPort = 0
        self.runThread = True
        socketThread = threading.Thread(target=self._create_test_socket)
        socketThread.start()
        time.sleep(1)
    
    @patch.object(ReciveUserInput,
                  "_send_to_server")
    def test_send_to_server(self, fakeSocket):
        reciveUserInput = ReciveUserInput('localhost', self.testSocketPort, 1)
        print('x')
        



    def _create_test_socket(self):
        tempSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tempSocket.bind(('localhost', 0))
        self.socketPort = tempSocket.getsockname()[1]
        conn = socket.socket()
        n = 0
        while(self.runThread): 
            tempSocket.listen(1)
            conn, addr = tempSocket.accept()
            n = n + 1
            if (n == 2):#One working ip addresses in _pre_defined_hosts_list_
                pass   #Two interfaces
                        #1 * 2 = Two connection requests.
        conn.shutdown(SHUT_RDWR)
        conn.close()
