import unittest
from unittest.mock import patch
import socket
from socket import SHUT_RDWR
import time
from PySide6.QtCore import QThreadPool
import threading
import struct
from pro_110822.reciveuserinput import ReciveUserInput
from pro_110822.prologging import Log

log = Log(20)

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

    def setUp(self):
        self.runTestServer = True
        serverThread = threading.Thread(target=self._create_test_server)
        serverThread.daemon = True
        serverThread.start()
        time.sleep(1)

    # def tearDown(self) -> None:
    #     log.debug("**STARTED**")
    #     self.runTestServer = False
    #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     s.connect(('localhost', self.testServerPort))
    #     s.shutdown(SHUT_RDWR)
    #     s.close()
    #     log.debug("**EXITED**")

    def _receive_n_bytes(self, n):
        log.debug("**STARTED**")
        data = ''.encode()
        while len(data) < n:
            chunk = self.testServerConnection.recv(n - len(data))
            if (chunk == ''.encode()):
                break
            data += chunk
        log.debug(f"**EXITE** with {data}")
        return data
    

    def _create_test_server(self):
        log.debug("**STARTED**")
        testServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        testServerSocket.bind(('localhost', 0))
        log.info(f"started testServerSocket {testServerSocket}")
        self.testServerPort = testServerSocket.getsockname()[1]
        
        log.debug("listning")
        testServerSocket.listen(1)
        log.debug("after listning")
        self.testServerConnection, _ = testServerSocket.accept()
        log.debug(f"accepted: {self.testServerConnection}")
        headerData = self._receive_n_bytes(4)
        dataLen = struct.unpack('<L', headerData)[0]
        data = self._receive_n_bytes(dataLen)
        data = data.decode()
        log.debug(f"recived {data}")

        clientIP = self.testServerConnection.getsockname()[0]
        self.testServerConnection.shutdown(SHUT_RDWR)
        self.testServerConnection.close()

        clientPort = data.split('!')[3]

        self.sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sendSocket.connect((clientIP, clientPort))



        log.debug("**EXITED**")

    def _send_message(self, message):
        message = message.encode()
        header = struct.pack('<L', len(message))
        self.testServerConnection.sendall(header + message)

    def test_recive_from_server(self):
        log.debug('')
        reciveUserInput = ReciveUserInput('localhost', str(self.testServerPort), 1)
        threabool = QThreadPool()
        threabool.setMaxThreadCount(5)
        threabool.start(reciveUserInput)
        time.sleep(1)
        print("")
        time.sleep(1)
        print("")
        self._send_message("Hello")
        time.sleep(1)
        print("")
        time.sleep(1)

        # try:
        #     self._send_message('hello')
        # except Exception:
        #     pass
        # # try:
        #     self._send_message('hello')
        # except Exception:
        #     pass
