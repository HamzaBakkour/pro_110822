import unittest
import unittest.mock
from unittest.mock import patch
from unittest.mock import Mock
from pro_110822.connectionsmonitor import ConnectionsMonitor
import socket, errno
import time
import threading


Pass = Mock()
Fail = socket.error

class TestConnectionsmonitor(unittest.TestCase):

    @patch.object(ConnectionsMonitor,
                  "_send_test_message",
                  side_effect = [Pass,
                                 Pass,
                                 Fail],
                  autospec=True)
    def test_socketError(self, fake_test_message):
            #test_socketError, pro_110822.connectionsmonitor.ConnectionsMonitor 
            #
            # ConnectionsMonitor takes a list of socket connections 
            #   iterates through them and test if they are vaild
            #   if a connection throwes a socket.error upon a sendall('*'.encode())
            #   the connection is closed and removed from the list
            #
            # This test function passes a list of three connections to ConnectionsMonitor
            #  the first two are dummy and they will pass
            #  the third is a valid socket connection and will fail

            dummySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            realSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            realSocket.bind(('localhost', 0))
            PORT = realSocket.getsockname()[1]

            connections = [{'connection': dummySocket},
                            {'connection': dummySocket},
                            {'connection': realSocket}]
            
            START_LEN = len(connections)
            
            connectionsMonitor = ConnectionsMonitor(connections)

            #Define a thread to terminate connectionsMonitor
            # after 5 seconds from its start.
            def _kill_after_a_while():
                time.sleep(5)
                connectionsMonitor.alive = False
            kill = threading.Thread(target=_kill_after_a_while)     
            kill.start()


            #Verify that realSocket's port is in use.
            self._assertPortInUse(PORT)
            self.assertEqual(len(connectionsMonitor.connectionsList), START_LEN)
            self.assertTrue(connectionsMonitor.alive)
            connectionsMonitor.run()
            self.assertFalse(connectionsMonitor.alive)
            self.assertEqual(connectionsMonitor._port, PORT)
            #Since realSocket's connection has failed ???
            # the connection should be closed and the port should now be available.
            self._assertPortNotInUse(PORT)
            #verify realSocket's connection has been removed.
            assert len(connectionsMonitor.connectionsList) == START_LEN - 1
            if ({'connection': realSocket} in connections):
                 self.fail("realSocket's connection should have failed\n" \
                           "and removrd from the connections list")
                 
    def _assertPortInUse(self, port):
            try:
                tempSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tempSocket.bind(('localhost', port))
            except socket.error as e:
                 assert e.errno == errno.EADDRINUSE
            else:
                 self.fail(f"PORT:{port} is available.")

    def _assertPortNotInUse(self, port):
            try:
                 tempSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                 tempSocket.bind(('localhost', port))
            except Exception:
                 self.fail(f"PORT:{port} is in use.\n")          
    

if __name__ == '__main__':
    unittest.main()

































































                 
    # def test_socketError(self, fake_test_message):
                    
    #         dummySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #         realSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         realSocket.bind(('localhost', 0))
    #         PORT = realSocket.getsockname()[1]

    #         connections = [{'connection': dummySocket},
    #                                 {'connection': dummySocket},
    #                                 {'connection': realSocket}]
            
    #         connectionsMonitor = ConnectionsMonitor(connections)
            
    #         def _kill():
    #             time.sleep(10)
    #             connectionsMonitor.alive = False

    #         kill = threading.Thread(target=_kill)     
    #         kill.start()

    #         assert len(connectionsMonitor.connectionsList) == len(connections)
    #         try:
    #              tempSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #              tempSocket.bind(('localhost', PORT))
    #         except socket.error as e:
    #              assert e.errno == errno.EADDRINUSE
    #         else:
    #              self.fail("PORT is available. It should not be.")
    #         connectionsMonitor.run()
    #         assert connectionsMonitor._port == PORT
    #         assert len(connectionsMonitor.connectionsList) == len(connections)

    #         try:
    #              tempSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #              tempSocket.bind(('localhost', PORT))
    #         except socket.error:
    #              self.fail("PORT is not available. It should be.")
                 



# import unittest
  
# class MyTestCase(unittest.TestCase):
  
#   # Returns true if 100 / 0 raises an Exception
#    def test_1(self):
#       with self.assertRaises(ZeroDivisionError):
#          100 / 0
  
# if __name__ == '__main__': 
#     unittest.main()


# import socket, errno

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try:
#     s.bind(("127.0.0.1", 5555))
# except socket.error as e:
#     if e.errno == errno.EADDRINUSE:
#         print("Port is already in use")
#     else:
#         # something else raised the socket.error exception
#         print(e)

# s.close()


# import socket

# sock.bind(('', 0))
# sock.getsockname()[1]

# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
# PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print(f"Connected by {addr}")
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             conn.sendall(data)    


#Run the test with dummy connections
# some of them will success and some of them will fail
#
#The first two will success and i want to make
# sure that they succeed 
#
#The third will fail and i want to make sure
# that the module got the right port
# emited the signal to the main thread
# closed the connection
# and removed it
#
#
#
#


# class TestConnectionsmonitor(unittest.TestCase):
#     def test_dum(self):
        
#         with unittest.mock.patch.object(ConnectionsMonitor, "_send_test_message", autospec=True) as fake_test_message:
#             Success = Mock()
#             Fail = socket.error

#             fake_test_message.side_effect = [Success, Success, Fail]
            
#             dummySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             x = ConnectionsMonitor([{'connection': dummySocket}])
#             x.run()