import unittest
from unittest.mock import patch
import socket
from socket import SHUT_RDWR
import threading
import time
import ipaddress
from ipaddress import IPv4Network

# pyright: reportGeneralTypeIssues=true

from pro_110822.portscanner import port_scanner, \
    get_active_interfaces, \
    get_hosts_list

_pre_defined_hosts_list_ = ['999.999.999.999',
                          '999.999.999.999',
                          '999.999.999.999',
                          '999.999.999.999',
                          '999.999.999.999',
                          '999.999.999.999',
                          '999.999.999.999',
                          'localhost',
                          '999.999.999.999',
                          '999.111.111.999']

_pre_defined_interfaces_list_ = [{'addr': 'fakeAddr_1', 'netmask': 'fakeNetmask_1'},
                               {'addr': 'fakeAddr_2', 'netmask': 'fakeNetmask_2'}]

class TestPortscanner(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.socketPort = 0

    @patch('pro_110822.portscanner.get_hosts_list',
                  return_value = _pre_defined_hosts_list_,
                  autospec=True)
    @patch('pro_110822.portscanner.get_active_interfaces',
                  return_value = _pre_defined_interfaces_list_,
                  autospec=True)
    def test_port_scanner(self, interfacesList, hostsList):
        #test_port_scanner, pro_110822.portscanner.port_scanner
        #
        # port_scanner checks if a TCP connection can be established
        # with local ip addresses on the hosts network
        #
        # This test function passes a list of pre-defined ip addresses
        # to port_scanner
        # two of these ip addresses are valid 
        # port_scanner should be able to estaplis a TCP connection with them

        socketThread = threading.Thread(target=self._create_test_socket)
        socketThread.start()
        time.sleep(1)
        PORT = self.socketPort
        self.failIf(PORT == 0)
        scann = port_scanner(PORT, 5, 0.1)
        numIteration = 0
        for entry in scann:
            match numIteration:
                case 0:
                    self.assertEqual(entry['pinged'], 5) 
                    self.assertEqual(entry['start_address'], '999.999.999.999')
                    self.assertEqual(entry['end_address'], '999.999.999.999')
                    self.assertEqual(len(entry['ping_ok']), 0)
                    self.assertEqual(len(entry['port_ok']), 0)
                    self.assertEqual(len(entry['peer_name']), 0)
                    self.assertEqual(entry['percentage'], '25.00%')
                case 1:
                    self.assertEqual(entry['pinged'], 5)
                    self.assertEqual(entry['start_address'], '999.999.999.999')
                    self.assertEqual(entry['end_address'], '999.111.111.999')
                    self.assertEqual(len(entry['ping_ok']), 1)
                    self.assertEqual(len(entry['port_ok']), 1)
                    self.assertGreater(len(entry['peer_name']), 0)
                    self.assertEqual(entry['percentage'], '50.00%')
                case 2:
                    self.assertEqual(entry['pinged'], 5)
                    self.assertEqual(entry['start_address'], '999.999.999.999')
                    self.assertEqual(entry['end_address'], '999.999.999.999')
                    self.assertEqual(len(entry['ping_ok']), 0)
                    self.assertEqual(len(entry['port_ok']), 0)
                    self.assertEqual(len(entry['peer_name']), 0)
                    self.assertEqual(entry['percentage'], '75.00%')
                case 3:
                    self.assertEqual(entry['pinged'], 5)
                    self.assertEqual(entry['start_address'], '999.999.999.999')
                    self.assertEqual(entry['end_address'], '999.111.111.999')
                    self.assertEqual(len(entry['ping_ok']), 1)
                    self.assertEqual(len(entry['port_ok']), 1)
                    self.assertGreater(len(entry['peer_name']), 0)
                    self.assertEqual(entry['est'], 0.0)
                    self.assertEqual(entry['percentage'], '100.00%')
            numIteration = numIteration + 1

    def test_get_active_interfaces(self):

        _active_interface_ = get_active_interfaces(False)
        self.assertGreater(len(_active_interface_),
                           0,
                           "get_active_interfaces returned 0 active interfaces.")
        for interface in _active_interface_:
            self.assertEqual(len(interface),4)
            self.assertEqual(ipaddress.ip_address(interface['addr']).version,
                             4,
                             f"{ipaddress.ip_address(interface['addr'])} is not\n" \
                             "a valid IPv4 address")
            self.assertIsInstance(interface['network'],
                                  ipaddress.IPv4Network,
                                  f"{interface['network']} is not\n" \
                                    "a valid IPv4 network")

    def test_get_hosts_list(self):
        result = get_hosts_list('192.168.0.15', '255.255.255.0')
        self.assertEqual(len(result), 254)
        self.assertEqual(result[0].compressed, '192.168.0.1')
        self.assertEqual(result[60].compressed, '192.168.0.61')
        self.assertEqual(result[120].compressed, '192.168.0.121')
        self.assertEqual(result[200].compressed, '192.168.0.201')
        self.assertEqual(result[253].compressed, '192.168.0.254')

    def _create_test_socket(self):
        tempSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tempSocket.bind(('localhost', 0))
        self.socketPort = tempSocket.getsockname()[1]
        conn = socket.socket()
        n = 0
        while(True): 
            tempSocket.listen(1)
            conn, addr = tempSocket.accept()
            n = n + 1
            if (n == 2):#One working ip addresses in _pre_defined_hosts_list_
                break   #Two interfaces
                        #1 * 2 = Two connection requests.
        conn.shutdown(SHUT_RDWR)
        conn.close()    
        
if __name__ == '__main__':
    unittest.main()