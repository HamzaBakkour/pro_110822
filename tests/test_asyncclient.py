import unittest
import socket
import threading
import time
from socket import SHUT_RDWR
from asyncio.exceptions import CancelledError
import pdb

from pro_110822.client.asyncclient import AsyncClient
from tests.timer import Timer

#connect to server at a given ip and port

#send and recive a message from the server

#recive an info request and send correct respond

#mouse and keyboard controller






class TestAsyncclient(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._server_socket_port = None
        self._server_socket_accepted_requsts = 0
        self._server_socket_recived_messages = []

    def test_connect_to_server(self):
        timer = Timer(2)
    
        timer.start()

        try:
            timer.join()
        except TimeoutError:
            self.fail('Test took too long...')



        client = AsyncClient()
        socketThread = threading.Thread(target=self._server_socket)

        socketThread.start()
        time.sleep(2)
        try:
            client.connect('127.0.0.1', self._server_socket_port)
        except CancelledError:
            pass
        
        self.assertEqual(self._server_socket_accepted_requsts, 1)
        self._server_socket_accepted_requsts = 0
        self._server_socket_port = None



    def test_send_message_to_server(self):
        # client = AsyncClient()
        # socketThread = threading.Thread(target=self._server_socket, args=(1,), 
        #                                 kwargs={'recive_message' : True,
        #                                         'to_be_recived' : 5})
        # socketThread.start()
        # time.sleep(2)
        # timer = Timer(1)
        # timer.start()

        # time.sleep(5)

        pass


    # def _timer_thread(self, time_):




    def _server_socket(self,
                       break_at = 1,
                       recive_message = False,
                       to_be_recived = 1,
                       send_message = False, 
                       to_be_sent = 1,
                       messages = []):
        self._server_socket_accepted_requsts = 0
        self._server_socket_port = None
        self._server_socket_recived_messages = []

        tempSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tempSocket.bind(('localhost', 0))
        self._server_socket_port = tempSocket.getsockname()[1]
        conn = socket.socket()
        while(True):
            tempSocket.listen(1)
            conn, addr = tempSocket.accept()
            self._server_socket_accepted_requsts +=  1
            # if recive_message:
                # for _ in range(1, to_be_recived):

            if (self._server_socket_accepted_requsts == break_at):#One working ip addresses in _pre_defined_hosts_list_
                break
        self.assertEqual(self._server_socket_accepted_requsts,
                         break_at)
        conn.shutdown(SHUT_RDWR)
        conn.close()
    

if __name__ == '__main__':
    unittest.main()







        # socketThread = threading.Thread(target=self._server_socket, args=(1,))
