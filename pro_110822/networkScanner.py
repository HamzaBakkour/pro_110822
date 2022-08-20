"""
This module is a network scanner. It allows the user
to optain the name and the ip address of connected devices
on the host's network.

The module contains the following functions:

- `get_host_ip_address()` - Returns the ip address of the host.
- `get_host_network_infterfaces_id()` - Returns the id of the host's network interfaces.
- `get_host_network_infterfaces_ipv4()` - Returns IPv4 addresses of the host's active network interfaces.
- `get_host_ipaddress__netmask__broadcast()` - Returns the host's IP address, netmask and boradcast address.
- `get_host_default_gateway()` - Returns the host's default gateway
- `get_prefix(ip_address, netmask)` - Returns the network portion of an IP address given its netmask.
- `get_network_address(ip_address, netmask)` -  Returns the network address of an IP address given its netmask.
- `get_host_network_info()` - Returns information about the host's network.
- `get_available_ip_addresses_on_host_network()` - Returns the IP address of the available devices on the host's network (Including the IP addresses of the host's own interfaces). 
- `get_ip_of_connected_devices_on_host_network()` - Returns the IP address of the available devices on the host's network (The IP addresses of the host's own interfaces are not included). 
- `get_connected_devices_name()-` - Returns the name and the IP address of the connected devices on the host's network.
"""

import netifaces
import socket
import networkscan
import ipaddress
from netaddr import IPNetwork

def get_host_ip_address()->str:
    """
    Returns the IP address of the host.

    Args:

    Rretuns:
        str: A string representing the IP address of the host.
    """
    return socket.gethostbyname(socket.gethostname())


def get_host_network_infterfaces_id()->list:
    """
    Returns the id of the host's network interfaces.

    Args:

    Returns:
        list: A list of the host's network interfaces ID. Each element in the list
            represents a network interface ID.
    """
    return  netifaces.interfaces()



def get_host_network_infterfaces_ipv4()->list:
    """
    Returns IPv4 addresses of the host's active network interfaces.

    Args:

    Returns:
        list: A list contains IPv4 address of the host's active network interfaces. 
            If the host have active interfaces using IPv6, they wont be included in the list.
    """
    #Get the network interfaces ID
    interfaces_id = get_host_network_infterfaces_id()
    interfaces_ipv4_addresses = []
    for interface_id in interfaces_id:
        try:#Pass each interface ID to netifaces.ifaddresses()
            #The number [2] means that the function will return a result only if
            #the interface has an IPv4 address. Hence the try except KeyError.
            #Use [23] insted of [2] if you want IPv6 address.
            #Do not use any number if you want to get all the addresses family.
            interfaces_ipv4_addresses.append(netifaces.ifaddresses(interface_id)[2])
        except KeyError:
            pass
    return interfaces_ipv4_addresses


def get_host_ipaddress__netmask__broadcast()->dict:
    """
    Returns the host's IP address, netmask and boradcast address.

    Args:

    Returns:
        dict: A dictionary of the form {'host_ip_address' : the_host_ipv4_address, 'host_netmask' : the_host_netmask, 'host_boradcast' : the_host_broadcast_address} 
    """
    host_ip_address = get_host_ip_address()
    active_interfaces_ipv4 = get_host_network_infterfaces_ipv4()
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



def get_host_default_gateway()->str:
    gateways = netifaces.gateways()
    host_gateway = ''
    for key in gateways.keys():
        if (key == 'default'):
            for keyy in gateways['default'].keys():
                host_gateway = gateways['default'][keyy][0]
    return host_gateway



def get_prefix(ip_address : str, netmask : str)->str:
    ip = IPNetwork(ip_address + '/' + netmask)
    return str(ip.prefixlen)


def get_network_address(ip_address : str, netmask : str)->str:
    ip_and_netmask = ip_address + '/' + netmask
    network = ipaddress.IPv4Network(ip_and_netmask, strict=False)
    return network.network_address.compressed


def get_host_network_info()-> dict:
    # host : ip address, netmask, broadcast, gateway, prefix, network address

    network_info = get_host_ipaddress__netmask__broadcast()
    network_info.update({'host_gateway' : get_host_default_gateway()})
    network_info.update({'host_prefix' : get_prefix(network_info['host_ip_address'] ,network_info['host_netmask'])})
    network_info.update({'host_network_address' : get_network_address(network_info['host_ip_address'], network_info['host_netmask'])})
    return network_info


def get_available_ip_addresses_on_host_network()->list:
    host_network_info = get_host_network_info()
    host_network = host_network_info['host_network_address'] + '/' + host_network_info['host_prefix']
    my_scan = networkscan.Networkscan(host_network)
    # Run the scan of hosts using pings
    my_scan.run()
    return my_scan.list_of_hosts_found


def get_ip_of_connected_devices_on_host_network()->list:
    host_network_info = get_host_network_info()
    available_ip_addresses_on_host_network = get_available_ip_addresses_on_host_network()

    ip_of_connected_devices = []
    for ip_address in available_ip_addresses_on_host_network:
        if ((ip_address != host_network_info['host_gateway']) and (ip_address != host_network_info['host_network_address'])):
            ip_of_connected_devices.append(ip_address)
    return ip_of_connected_devices


def get_connected_devices_name()->list:
    connected_devices_ip = get_ip_of_connected_devices_on_host_network()
    connected_devices_name__ip = []
    for device_ip in connected_devices_ip:
        try:
            connected_devices_name__ip.append(socket.gethostbyaddr(device_ip))
        except:
            print ('could not get the name of : {}\n'.format(device_ip))

    return sorted(connected_devices_name__ip)


# print(get_available_ip_addresses_on_host_network())
# print(get_ip_of_connected_devices_on_host_network())
# print(get_connected_devices_name())

