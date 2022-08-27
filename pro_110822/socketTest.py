# import subprocess  # For executing a shell command
# import asyncio

# async def ping_asyc(host_first):
#     host_last = 1
#     ping_list = []
#     while(host_last < 20):
#         host = host_first + '.' + str(host_last)
#         print(host)
#         command = ['ping', "-n", '1', '-w','50', host]
#         # await print(host, (subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0))
#         if(subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0):
#             ping_list.append(host)
#         await asyncio.sleep(10)
#         host_last = host_last + 1
#     print(ping_list)
#     # return(ping_list)


# loop = asyncio.get_event_loop()
# loop.run_until_complete(ping_asyc("192.168.0"))
# loop.close()

# import subprocess  # For executing a shell command

# def ping_asyc(host_first):
#     host_last = 1
#     ping_list = []
#     while(host_last < 20):
#         host = host_first + '.' + str(host_last)
#         print(host)
#         command = ['ping', "-n", '1', '-w','50', host]
#         # await print(host, (subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0))
#         if(subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0):
#             ping_list.append(host)
#         host_last = host_last + 1
#     print(ping_list)
#     # return(ping_list)

# ping_asyc("192.168.0")


