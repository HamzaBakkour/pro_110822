import unittest
from unittest.mock import patch
import socket
from socket import SHUT_RDWR
import time
from PySide6.QtCore import QThreadPool
import threading
import struct
from pro_110822.reciveuserinput import ReciveUserInput


_actions_ = []
def _append_action(action):
    _actions_.append(action)


#Send input to ReicveInput
#check that recive input is passing
#the right instruction to mouse and keyboard controlers


class TestReciveuserinput(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.testServerPort = 0
        self.runTestServer = True
        self.testServerConnection = socket.socket()
        # socketThread = threading.Thread(target=self._create_test_socket)
        # # socketThread.start()
        # time.sleep(1)


    def setUp(self):
        self.runTestServer = True
        serverThread = threading.Thread(target=self._create_test_server)
        serverThread.start()
        time.sleep(1)

    def tearDown(self) -> None:
        self.runTestServer = False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', self.testServerPort))
        s.shutdown(SHUT_RDWR)
        s.close()


    def _create_test_server(self):
        testServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        testServerSocket.bind(('localhost', 0))
        self.testServerPort = testServerSocket.getsockname()[1]
        while(self.runTestServer): 
            testServerSocket.listen(1)
            self.testServerConnection, _ = testServerSocket.accept()
        self.testServerConnection.shutdown(SHUT_RDWR)
        self.testServerConnection.close()

    def _send_message(self, message):
        message = message.encode()
        header = struct.pack('<L', len(message))
        self.testServerConnection.sendall(header + message)

    def test_recive_from_server(self):
        reciveUserInput = ReciveUserInput('localhost', str(self.testServerPort), 1)
        threabool = QThreadPool()
        threabool.setMaxThreadCount(5)
        threabool.start(reciveUserInput)
        time.sleep(1)
        try:
            self._send_message('hello')
        except:
            pass
        try:
            self._send_message('hello')
        except Exception as ex:
            v = type(ex)
            print('x')
        try:
            self._send_message('hello')
        except:
            pass

        reciveUserInput.alive = False
        try:
            self._send_message('hello')
        except:
            pass
        print('x')
        


