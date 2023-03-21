import unittest
from unittest.mock import patch
import socket
from socket import SHUT_RDWR
import time
from PySide6.QtCore import QThreadPool
import threading
import struct
from pro_110822.reciveuserinput import ReciveUserInput


# from PySide6.QtCore import QThreadPool, SIGNAL
# self.threabool = QThreadPool()
# self.threabool.setMaxThreadCount(25)
# self.threabool.start(self.reciveMouseMovementWorkers[-1])


    # def __init__(self, methodName: str = "runTest") -> None:
    #     super().__init__(methodName)
    #     self.testSocketPort = 0
    #     self.runThread = True
    #     socketThread = threading.Thread(target=self._create_test_socket)
    #     socketThread.start()
    #     time.sleep(1)

class TestReciveuserinput(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.testSocketPort = 0
        self.runThread = True
        self.conn = socket.socket()
        # socketThread = threading.Thread(target=self._create_test_socket)
        # # socketThread.start()
        # time.sleep(1)


    def setUp(self):
        self.runThread = True
        socketThread = threading.Thread(target=self._create_test_socket)
        socketThread.start()
        time.sleep(1)

    def tearDown(self) -> None:
        self.runThread = False
        tempSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tempSocket.connect(('localhost', self.testSocketPort))
        tempSocket.shutdown(SHUT_RDWR)
        tempSocket.close()




    def _create_test_socket(self):
        tempSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tempSocket.bind(('localhost', 0))
        self.testSocketPort = tempSocket.getsockname()[1]
        while(self.runThread): 
            tempSocket.listen(1)
            self.conn, addr = tempSocket.accept()
        self.conn.shutdown(SHUT_RDWR)
        self.conn.close()

    def _send_message(self, message):
        message = message.encode()
        header = struct.pack('<L', len(message))
        self.conn.sendall(header + message)


    def test_recive_from_server(self):
        reciveUserInput = ReciveUserInput('localhost', str(self.testSocketPort), 1)
        threabool = QThreadPool()
        threabool.setMaxThreadCount(5)
        threabool.start(reciveUserInput)
        self._send_message('hello')
        reciveUserInput.alive = False
        print('x')
        



    # def _create_test_socket(self):
    #     tempSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     tempSocket.bind(('localhost', 0))
    #     self.socketPort = tempSocket.getsockname()[1]
    #     conn = socket.socket()
    #     n = 0
    #     while(self.runThread): 
    #         tempSocket.listen(1)
    #         conn, addr = tempSocket.accept()
    #         n = n + 1
    #         if (n == 2):#One working ip addresses in _pre_defined_hosts_list_
    #             pass   #Two interfaces
    #                     #1 * 2 = Two connection requests.
    #     conn.shutdown(SHUT_RDWR)
    #     conn.close()
