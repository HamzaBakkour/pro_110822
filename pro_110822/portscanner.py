import asyncio
import time
import socket
import ipaddress
import os
import inspect
try:
    import netifaces
except ModuleNotFoundError as ex:
    print('\n************************************************************************')
    print(f'{ex}\nYou can not use the function "port_scanner" without installing netifaces.\nPlease install netifaces or use "port_scanner_" instead!')
    print('************************************************************************\n')


"""
-------------------------------------------------------------------------------------------------
portscanner.py by Hamza Bakkour. alexander.x4.hb@outlook.com

What is this?
    A port scanner. This script checks if a TCP connection can be 
    istablished with any of the available devices on the host's network.

How to use it?
    There are two ways to use this script:
    [1] port_scanner(port : int, groupSize : int, rest : int | float)
    [2] port_scanner_(port : int, ipAndNetmask : list[str] | str, gourpMembers : int, rest : int | float)

    [1] port_scanner(port : int, groupSize : int, rest : int | float)
        This function requires installing the external module netifaces. *
        Arguments:
            port : (int)  The port that you are trying to establish a TCP connection with.
            groupSize : (int) The function will ping all the ip addresses in the host's network.
                                 However, not all ip addresses  are pinged at once. Since this will
                                 stress the CPU.  Especially  that -  depending on how many network 
                                 interfaces you have  and  what  type of netowrk each  interafce is 
                                 connected to - there can be  a thousends of ip addresses that need
                                 to be pinged.  Instead,  the  ip addresses are divided into groups
                                 and each group is pinged at once with a sleep time between each group.
                                 This argument determine the groups size.
            rest : (int | float) : A sleep time between each group-ping.

    [2] port_scanner_(port : int, ipAndNetmask : list[str] | str, gourpMembers : int, rest : int | float)
        This function does not use any external modules.
        Arguments:
            port : (int)  The same as port_scanner.
            ipAndNetmask : (list[str] | str) This function does not use  the external module  netifaces
                                             to  get  the  the  ip  address  and  network  mask of each 
                                             network interface. Instead, you have to pass them manually
                                             in the form of 'ip_address/netmask'.
            groupSize : (int)  The same as port_scanner.
            rest : (int | float) : The same as port_scanner.

What does it return?
    Both "port_scanner" and "port_scanner_" return a generator.
    The following exaample shows the output of running "port_scanner_"
    on my PC. I first  used  CMD  and the command ipconfig to list the 
    network  interfaces  and  thier ip addresses. Then i passed the ip
    address and network  mask  of  one of the interfaces (you can pass
    a list of 'ip_address/netmask'). I chosed to group the ip addresses
    into a groups of 25.  And i told the script  to  sleep  one second 
    between pinging each group.


    import portscanner

    scan = portscanner.port_scanner_(12345, ['192.168.0.25/255.255.255.0'] ,25, 1)

    for entry in scan:
        print(entry)

    #Output
    {'pinged': 25, 'start_address': '192.168.0.1', 'end_address': '192.168.0.25', 'time': '2.81', 'ping_ok': ['192.168.0.1', '192.168.0.6', '192.168.0.11', '192.168.0.14', '192.168.0.25'], 'port_ok': ['192.168.0.14'], 'est': 28.13, 'percentage': '9.09%'}
    {'pinged': 25, 'start_address': '192.168.0.26', 'end_address': '192.168.0.50', 'time': '1.39', 'ping_ok': [], 'port_ok': [], 'est': 12.48, 'percentage': '18.18%'}
    {'pinged': 25, 'start_address': '192.168.0.51', 'end_address': '192.168.0.75', 'time': '1.50', 'ping_ok': [], 'port_ok': [], 'est': 11.99, 'percentage': '27.27%'}
    {'pinged': 25, 'start_address': '192.168.0.76', 'end_address': '192.168.0.100', 'time': '1.50', 'ping_ok': [], 'port_ok': [], 'est': 10.5, 'percentage': '36.36%'}
    {'pinged': 25, 'start_address': '192.168.0.101', 'end_address': '192.168.0.125', 'time': '2.16', 'ping_ok': ['192.168.0.107'], 'port_ok': [], 'est': 12.98, 'percentage': '45.45%'}
    {'pinged': 25, 'start_address': '192.168.0.126', 'end_address': '192.168.0.150', 'time': '1.34', 'ping_ok': [], 'port_ok': [], 'est': 6.68, 'percentage': '54.55%'}
    {'pinged': 25, 'start_address': '192.168.0.151', 'end_address': '192.168.0.175', 'time': '1.50', 'ping_ok': [], 'port_ok': [], 'est': 6.0, 'percentage': '63.64%'}
    {'pinged': 25, 'start_address': '192.168.0.176', 'end_address': '192.168.0.200', 'time': '1.50', 'ping_ok': [], 'port_ok': [], 'est': 4.5, 'percentage': '72.73%'}
    {'pinged': 25, 'start_address': '192.168.0.201', 'end_address': '192.168.0.225', 'time': '1.55', 'ping_ok': [], 'port_ok': [], 'est': 3.11, 'percentage': '81.82%'}
    {'pinged': 25, 'start_address': '192.168.0.226', 'end_address': '192.168.0.250', 'time': '1.45', 'ping_ok': [], 'port_ok': [], 'est': 1.45, 'percentage': '90.91%'}
    {'pinged': 4, 'start_address': '192.168.0.251', 'end_address': '192.168.0.254', 'time': '1.49', 'ping_ok': [], 'port_ok': [], 'est': 0.0, 'percentage': '100.00%'}
    #End of output

    We see that each iteration yield i dictonary with the following keys:
    'pinged': The number of ip addresses that were pinged (The group size).
    'start_address': The first ip address in the group.   
    'end_address': The last ip address in the group.
    'time': The time - in seconds -it took to ping this group of ip addresses.
            This includes  pinging  the addresses and waiting for a respons.
            For exampld, we see that it took 2.81 seconds to ping the first
            group and 1.39 seconds to ping the second.
    'ping_ok': A list of the ip addresses that reponded to the ping.
    'port_ok': A list of the ports that reponded to the ping. In our case the
               ip address 192.168.0.14 i.e., 192.168.0.14:12345.
    'est': The estimated time that the script will take to finish. This 
           time is passed on the current iteration data.
    'percentage': Work progress.
-------------------------------------------------------------------------------------------------
* installing netifaces  
"""


"No duplicat, A function that returns a device name"


async def _async_ping(address : tuple[str, int]) -> tuple[str, int, int]:

    cmd = 'ping -n 1 ' + address[0]

    proc = await asyncio.create_subprocess_shell(
        cmd,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    if ('TTL' in stdout.decode()):
        return address + (1,)
    elif (stderr.decode() != ''):
        return address + (-1,)
    else:
        return address + (0,)


async def _chain_ip_and_port_ping(address : tuple[str, int]) -> tuple[str, int, int] | tuple[str, int, int, int]:
    pingResult = await _async_ping(address)

    if (pingResult[2] == 1):
        address = address + (1,)
        try:
            _ , writer = await asyncio.wait_for(asyncio.open_connection(address[0], address[1]), timeout=5)

        except socket.error:
            address = pingResult + (0,)
        except asyncio.exceptions.TimeoutError:
            address = pingResult + (0,)
        except Exception as ex:
            raise SystemExit(f'{ex}')
        else:
            address = pingResult + (1,)
            peerName = socket.gethostbyaddr(address[0])[0]
            if (len(peerName) > 0):
                address = address + (peerName,)
            else:
                address = address + ('Unknown',)
            writer.close()
            await writer.wait_closed()
            try:
                peerName = socket.gethostbyaddr(address[0])[0]
            except socket.error:
                address = address + ('Unknown',)
            else:
                if (len(peerName) > 0):
                    address = address + (peerName,)
                else:
                    address = address + ('Unknown',)
    else:
        address = pingResult
    return address  


async def _main_chain_ip_and_port_ping(args : list[tuple[str, int]]) -> list[tuple[str, int, int] | tuple[str, int, int, int]] :
    result = await asyncio.gather(*(_chain_ip_and_port_ping(n) for n in args))
    return(result)


def wrapper_to_main_chain_ip_and_port_ping(ip_addresses : list[tuple[str, int]] , groupMax : int, rest : int) -> dict[int, str, str, str, list[str], list [str], float, str]:
    GROUP_MAX = groupMax
    totalNum = len(ip_addresses)
    groups = []
    tempList = []

    threshold = GROUP_MAX

    n = 0
    for ip_addresse in ip_addresses:
        threshold = threshold - 1
        n = n + 1
        tempList.append(ip_addresse)
        if ((threshold <= 0) or (n == totalNum)):
            groups.append(tempList)
            tempList = []
            threshold = GROUP_MAX

    groupScanned = 0

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    for group in groups:
        start = time.perf_counter()
        grouResult = loop.run_until_complete(_main_chain_ip_and_port_ping(group))
        end = time.perf_counter() - start

        groupScanned = groupScanned + 1
        percentage = (100* int(len(group))/(len(group) * len(groups)))

        # for el in grouResult:
        #     print(el)

        # for el in grouResult:
        #     print(el)

        yield {'pinged' : len(group), 
            'start_address' : group[0][0],
            'end_address' : group[-1][0],
            'time' : f'{end:0.2f}', 
            'ping_ok' : [i[0] for i in grouResult if(i[2] == 1)],
            'port_ok' : [i[0] for i in grouResult if((len(i) == 5) and (i[3] == 1))],
            'peer_name': [i[4] for i in grouResult if((len(i) == 5) and (i[3] == 1))],
            'port_ok' : [i[0] for i in grouResult if((len(i) == 5) and (i[3] == 1))],
            'peer_name': [i[4] for i in grouResult if((len(i) == 5) and (i[3] == 1))],
            'est' : round(end * (len(groups) - groupScanned), 2),
            'percentage' : f'{(percentage * groupScanned):0.2f}%'
            }
        time.sleep(rest)


def get_active_interfaces(duplicates : bool = False)->list[dict[str, str, str, ipaddress.IPv4Network]]:
    ipV4 = 2
    ipV6 = 23
    active = []
    ipSocket = socket.gethostbyname(socket.gethostname())
    active.append({'addr' : ipSocket})
    interfaces_id = netifaces.interfaces()

    for interface_id in interfaces_id:
        try:
            if (ipV4 in netifaces.ifaddresses(interface_id).keys()):
                if (netifaces.ifaddresses(interface_id)[ipV4][0]['addr'] != '127.0.0.1' ):#127.0. 0.1 (loopback address).
                    if (netifaces.ifaddresses(interface_id)[ipV4][0]['addr'] == ipSocket):
                        netmask = netifaces.ifaddresses(interface_id)[ipV4][0]['netmask']
                        broadcast = netifaces.ifaddresses(interface_id)[ipV4][0]['broadcast']
                        network = ipaddress.IPv4Network(netifaces.ifaddresses(interface_id)[ipV4][0]['addr'] + '/' + netifaces.ifaddresses(interface_id)[ipV4][0]['netmask'], strict=False)

                        active[0].update({'netmask' : netmask, 'broadcast' : broadcast, 'network' : network})
                    else:
                        active.append(netifaces.ifaddresses(interface_id)[ipV4][0])
                        network = ipaddress.IPv4Network(active[-1]['addr'] + '/' + active[-1]['netmask'], strict=False)
                        active[-1].update({'network' : network})
            else:
                continue

        except Exception as ex:
            print(f'{os.path.basename(__file__)} || ', f'{inspect.stack()[0][3]} || ', f'Exception raised: {ex}')

    #Remove duplicates.i.e, interfaces that have the same network address and netmask
    seen = set()
    activeNoDuplicates = []
    for el in active:
        t = tuple(el.items())
        if t[3] not in seen:
            seen.add(t[3])
            activeNoDuplicates.append(el)

    if duplicates:
        return active
    else:
        return activeNoDuplicates


def get_hosts_list(ipAddress : str, netmask : str)-> list[str]:
    ipAndPrefix = ipaddress.ip_interface(ipAddress + '/' + netmask)
    networkAddress = ipAndPrefix.network
    return list(networkAddress.hosts())


def port_scanner(port : int, groupSize : int, rest : int | float) -> dict[int, str, str, str, list[str], list [str], float, str]:
    interfaces = get_active_interfaces()
    allHosts = []
    for interface in interfaces:
        hosts = get_hosts_list(interface['addr'], interface['netmask'])
        for host in hosts:
            allHosts.append((str(host), port))
    scanResult = wrapper_to_main_chain_ip_and_port_ping(allHosts, groupSize, rest)

    return scanResult



def port_scanner_(port : int, ipAndNetmask : list[str] | str, groupSize : int, rest : int | float) -> dict[int, str, str, str, list[str], list [str], float, str]:
    allHosts = []
    if(isinstance(ipAndNetmask, str)):
        hosts = get_hosts_list(ipAndNetmask.split('/')[0], ipAndNetmask.split('/')[1])
        for host in hosts:
            allHosts.append((str(host), port))
        scanResult = wrapper_to_main_chain_ip_and_port_ping(allHosts, groupSize, rest)
        return scanResult

    elif (isinstance(ipAndNetmask, list)):
        for address in ipAndNetmask:
            if (isinstance(address, str)):
                hosts = get_hosts_list(address.split('/')[0], address.split('/')[1])
                for host in hosts:
                    allHosts.append((str(host), port))
            else:
                raise SystemExit(f'The argument "{address}" is of type {type(ipAndNetmask)}\nstr is required!')

        scanResult = wrapper_to_main_chain_ip_and_port_ping(allHosts, groupSize, rest)
        return scanResult
    
    else:
        raise SystemExit(f'The argument "{ipAndNetmask}" is of type {type(ipAndNetmask)}\nlist[str] or str are required!')
    
