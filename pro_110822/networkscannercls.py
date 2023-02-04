"""
This module is a network scanner. It allows the user
to optain the name and the ip address of the connected devices
on the local network.
"""

import netifaces
import socket
import networkscan
import ipaddress
from netaddr import IPNetwork
import subprocess
import asyncio

import sys
import os
import traceback
import logging
import time
import re

import pdb

from asyncioping import main_ping

class NetWrokScanner():
    def __init__(self):
        pass
    

    def get_host_ip_address(self)->str:
        return socket.gethostbyname(socket.gethostname())
        
    def get_host_network_infterfaces_id(self)->list:
        return  netifaces.interfaces()
        
    def get_host_network_infterfaces_ipv4(self)->list:
        #Get the network interfaces ID
        interfaces_id = self.get_host_network_infterfaces_id()
        interfaces_ipv4_addresses = []
        for interface_id in interfaces_id:
            try:#Pass each interface ID to netifaces.ifaddresses()
                #The number [2] means that the function will return a result only if
                #the interface has an IPv4 address. Hence the try except KeyError.
                #Use [23] insted of [2] if you want IPv6 address.
                #Do not use any number if you want to get all the addresses family.
                if (2 in netifaces.ifaddresses(interface_id).keys()):
                    interfaces_ipv4_addresses.append(netifaces.ifaddresses(interface_id)[2])
                else:
                    continue
            except KeyError:
                part1 = str(sys.exc_info())
                part2 = traceback.format_exc()
                origin = re.search(r'File(.*?)\,', part2).group(1) 
                loggMessage = origin + '\n' + part1  + '\n' + part2
                logging.info(loggMessage)
        return interfaces_ipv4_addresses

    def get_host_ipaddress_netmask_broadcast(self)->dict:
        host_ip_address = self.get_host_ip_address()
        active_interfaces_ipv4 = self.get_host_network_infterfaces_ipv4()
        host_netmask = ''
        host_boadcast = ''
        
        for element in active_interfaces_ipv4:
            for elements in element:
                if (elements['addr'] == host_ip_address):
                    host_netmask = elements['netmask']
                    host_boadcast = elements['broadcast']
                    if (host_netmask != None and host_boadcast != None):
                        break
        return {'host_ip_address' : host_ip_address, 'host_netmask' : host_netmask, 'host_boradcast' : host_boadcast}
        
    def get_host_default_gateway(self)->str:
        gateways = netifaces.gateways()
        host_gateway = ''
        for key in gateways.keys():
            if (key == 'default'):
                for keyy in gateways['default'].keys():
                    host_gateway = gateways['default'][keyy][0]
        return host_gateway



    def get_prefix(self, ip_address : str, netmask : str)->str:
        ip = IPNetwork(ip_address + '/' + netmask)
        return str(ip.prefixlen)


    def get_network_address(self, ip_address : str, netmask : str)->str:
        ip_and_netmask = ip_address + '/' + netmask
        network = ipaddress.IPv4Network(ip_and_netmask, strict=False)
        return network.network_address.compressed


    def get_host_network_info(self)-> dict:
        # host : ip address, netmask, broadcast, gateway, prefix, network address

        network_info = self.get_host_ipaddress_netmask_broadcast()
        network_info.update({'host_gateway' : self.get_host_default_gateway()})
        network_info.update({'host_prefix' : self.get_prefix(network_info['host_ip_address'] ,network_info['host_netmask'])})
        network_info.update({'host_network_address' : self.get_network_address(network_info['host_ip_address'], network_info['host_netmask'])})
        return network_info


    def get_arp(self)->list:
        arp_list = []

        arp_list = subprocess.check_output(("arp", "-a"))
        arp_list = arp_list.decode()
        arp_list = arp_list.split('\n')

        return arp_list


    def get_local_addresses_from_arp(self):
        netWorkInfo = self.get_host_network_info()
        arp_list = self.get_arp()
        local_ip = []

        host_network_range = netWorkInfo['host_netmask'].count('255.')
        host_ip_actual = ''
        host_ip_list = netWorkInfo['host_ip_address'].split('.')

        for i in range (0, host_network_range):
            host_ip_actual = host_ip_actual + host_ip_list[i] + '.'       

        for line in arp_list:
            line = line.lstrip()
            if (line.startswith(host_ip_actual)):
                local_ip.append(line.split(' ')[0])
        local_ip = list(dict.fromkeys(local_ip))

        return local_ip

    def get_local_addresses_from_ping(self):
        networkInfo = self.get_host_network_info()
        firstThreeOctate = networkInfo['host_ip_address'].replace(networkInfo['host_ip_address'].split('.')[3], '')[:-1]
        pingResult = asyncio.run(main_ping(firstThreeOctate))
        result = [i for i in pingResult if (i != networkInfo['host_ip_address'])]
        return result



    def get_ip_of_connected_devices_on_host_network(self)->list:
        host_network_info = self.get_host_network_info()
        available_ip_addresses_on_host_network = self.get_local_addresses_from_ping()

        ip_of_connected_devices = []
        for ip_address in available_ip_addresses_on_host_network:
            if ((ip_address != host_network_info['host_gateway']) and (ip_address != host_network_info['host_network_address'])):
                ip_of_connected_devices.append(ip_address)
        return ip_of_connected_devices


    def get_connected_devices_name(self)->list:
        connected_devices_ip = self.get_ip_of_connected_devices_on_host_network()
        connected_devices_name__ip = []
        for device_ip in connected_devices_ip:
            try:
                connected_devices_name__ip.append(socket.gethostbyaddr(device_ip))
            except:
                # part1 = str(sys.exc_info())
                # part2 = traceback.format_exc()
                # origin = re.search(r'File(.*?)\,', part2).group(1) 
                # loggMessage = origin + '\n' + part1  + '\n' + part2
                # print("***********************************************")
                # print("This was supposed to be a log message")
                # print("It creates a dummy,")
                # print("Message is: ")
                # print(loggMessage)
                # print("***********************************************")
                # logging.info(loggMessage)
                pass

        return sorted(connected_devices_name__ip)



# x = NetWrokScanner()
# x.get_local_addresses_from_ping()
# print(x.get_connected_devices_name())