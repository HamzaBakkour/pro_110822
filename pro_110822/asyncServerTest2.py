import asyncio
from asyncio.exceptions import CancelledError
import queue
from senduserinput import SendUserInput
import pdb

class AsyncServer():
    def __init__(self, ip, port) -> None:
        self.tasks_group = None
        self.server_coro = None
        self.ip = ip
        self.port = port
        self._writer = None
        self._reader = None
        self.inbound_queue = queue.Queue(maxsize=100)
        self.clients_queue = []
        self._capture_input = SendUserInput()
        self.stream = False
        self._send_data_s1_ = 0.1
        self._recive_data_s1_ = 0.1
        self._recive_data_s2_ = 0.5
        self._connections_monitor_s1_ = 0.1
        self._connections_monitor_s2_ = 1
        self._start_stream_s1_ = 0.1
        self._start_stream_s2_ = 1

    def send_data(self, data):
        asyncio.run(self._send_data(data))




    def start_stream(self):
        self._capture_input.start_listning()
        self.stream = True





    def stop_stream(self):
        self.stream = False
        self._capture_input.stop_listning()




    def set_client(self, clientIP, clientPort):
        temp = self._connected_clients_all()
        for client in temp:
            if ((client['addr'][0] == clientIP) and (client['addr'][1] == clientPort)):
                self._reader =  client['reader']
                self._writer =  client['writer']
                print(f"streaming to client {client['addr'][0]}:{client['addr'][1]}")
                return
        print(f"could not fined client {client['addr'][0]}:{client['addr'][1]} in connected clients.")





    def connected_clients(self):
         temp = []
         for item in self.clients_queue:
              temp.append(item['addr'])
         return  temp




    def recived_messages(self):
         return  list(self.inbound_queue.queue)




    def run(self):
         asyncio.run(self._main())





    def close(self):
        self.server_coro.close()
        try:
            asyncio.run(self.server_coro.wait_closed())
        except Exception as ex:
            print('in AsyncServer, close, ' ,ex, type(ex))
        self.tasks_group.cancel()





    def _connected_clients_all(self):
        return self.clients_queue





    def _add_to_inbound (self, data):
        if (len(data) > 0):
            print(f"added {data} to inbound queue")
            self.inbound_queue.put(data)





    async def _send_data(self, data):
            if (self._writer == None):
                print("no client was set. use set_client to set one.")
                return
            try:
                self._writer.write(data.encode())
                await self._writer.drain()
            except ConnectionResetError:
                print('ConnectionResetError')
                await asyncio.sleep(self._send_data_s1_)
            except Exception as ex:
                    print(type(ex), ex, 'Unhandeled')





    async def _start_stream(self):
        while(True):
            if (self.stream): 
                for _ in range(self._capture_input.events_queue.qsize()):
                    item = self._capture_input.events_queue.get()
                    await self._send_data(item)
                await asyncio.sleep(self._start_stream_s1_)
            else:
                await asyncio.sleep(self._start_stream_s2_)





    async def _recive_data(self):
        while(True):
            connections = self._connected_clients_all()
            for connection in connections:
                try:
                    data = await connection['reader'].read(100)
                    message = data.decode()
                    self._add_to_inbound(message)
                except Exception as ex:
                    print(f'in _recive_data {type(ex)}, {ex}')
                await asyncio.sleep(self._recive_data_s1_)
            await asyncio.sleep(self._recive_data_s2_)





    async def _connections_monitor(self):
        while(True):
            connections = self._connected_clients_all()
            for connection in connections:
                try:
                    connection['writer'].write(' '.encode())
                    await connection['writer'].drain()
                except Exception as ex:
                    print('in _connections_monitor ',  connection['addr'], type(ex), ' ', ex, ' [CLOSED]')
                    try:
                        connection['writer'].close()
                        await connection['writer'].wait_closed()
                    except ConnectionAbortedError:
                        pass
                    except ConnectionResetError:
                        pass
                    except Exception as ex:
                        print('in _connections_monitor ', type(ex), ' ', ex)
                    connections.remove(connection)
                await asyncio.sleep(self._connections_monitor_s1_)
            await asyncio.sleep(self._connections_monitor_s2_)







    async def _handler(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"{addr!r} is connected.")
        self.clients_queue.append({'addr' : addr, 'writer' : writer, 'reader' : reader})




    async def _start_server(self):
        self.server_coro = await asyncio.start_server(self._handler, self.ip, self.port)
        async with self.server_coro:
            try:
                await self.server_coro.serve_forever()
            except CancelledError:
                print('server_coro apported', CancelledError)





    async def _main(self):
        tasks = []
        tasks.append(asyncio.create_task(self._start_server()))
        tasks.append(asyncio.create_task(self._recive_data()))
        tasks.append(asyncio.create_task(self._connections_monitor()))
        tasks.append(asyncio.create_task(self._start_stream()))

        self.tasks_group = asyncio.gather(*tasks)
        try:
            await self.tasks_group
        except CancelledError:
            print('tasks_group cancelled', CancelledError)















































































# Listen for connections
# Accept connections and emmit to the mainwindow
# Send mouse and keyboard input
# Send managment data
# Recive managment data
# Connections monitor
        










    # def send_data(self, data):
    #     self._outbound_queue.put(data)
        


    # async def _send_data(self):
    #         while(True):
    #             if (self._writer == None):
    #                 await asyncio.sleep(0.5)
    #                 continue
    #             try:
    #                 item = self._outbound_queue.get(block=False)
    #                 self._writer.write(item.encode())
    #                 await self._writer.drain()
    #                 await asyncio.sleep(0.1)
    #             except queue.Empty:
    #                  await asyncio.sleep(0.5)
    #                  continue
    #             except ConnectionResetError:
    #                 print('ConnectionResetError')
    #                 await asyncio.sleep(0.1)
    #             except Exception as ex:
    #                  print(type(ex), ex, 'Unhandeled')


# async def _connections_monitor(self):
#      while(True):
#         for client in self.clients_queue:
#             clientIP = client[0]
#             clientPort = client[1]
#             print(f"clientIP: {clientIP}  clientPort: {clientPort}")
#             print(client)
#             try:
#                 await asyncio.open_connection(clientIP, clientPort)
#             except Exception as ex:
#                 print('connections monitor ', type(ex), ex, ' closing')
#             await asyncio.sleep(0.1)
#         await asyncio.sleep(1)

# tasks.append(asyncio.create_task(self._connections_monitor()))



# except ConnectionRefusedError:
#     pass

# self._writer.close()
# await self._wait_on_connection_close()
# async def _wait_on_connection_close(self):
#     try:
#         print("waiting on connection close")
#         await self._writer.wait_closed()
#     except ConnectionAbortedError:
#          pass
#     print("connection closed")



# server = Server('127.0.0.1', 8888)
# print("1")
# server.run()
# print("2")
# server.send_data("yes")


# server.send_data('yes')

# async def handle_echo(reader, writer):
#     data = await reader.read(100)
#     message = data.decode()
#     addr = writer.get_extra_info('peername')

#     print(f"Received {message!r} from {addr!r}")

#     print(f"Send: {message!r}")
#     writer.write(data)
#     await writer.drain()

#     print("Close the connection")
#     writer.close()
#     await writer.wait_closed()

# async def main():
#     server = await asyncio.start_server(
#         handle_echo, '127.0.0.1', 8888)

#     addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
#     print(f'Serving on {addrs}')

#     async with server:
#         await server.serve_forever()

# asyncio.run(main())



# await asyncio.gather(await asyncio.start_server(self.listen_for_connections, self.IP , self.Port),
#                      await self.send_data('hello'),
#                      await self.close_connection())


# class Server():
#     def __init__(self, ip, port) -> None:
#         self.IP = ip
#         self.Port = port
#         self._writer = None

#     async def _handler(self, reader, writer):
#         self._writer = writer
#         data = await reader.read(100)
#         message = data.decode()
#         addr = self._writer.get_extra_info('peername')

#         print(f"Received {message!r} from {addr!r}")

#     async def _send_data(self, data):
#             await asyncio.sleep(2)
#             print(f"Send: {data!r}")
#             self._writer.write(data)
#             await self._writer.drain()

#     async def close_connection(self):
#             print("Close the connection")
#             self._writer.close()
#             await self._writer.wait_closed()

#     def send_data(self, data):
#         pool = Pool(processes=1)              
#         # pool.apply_async(self.send_data, ['yes'], callback) 
#         pool.apply_async(self._send_data, [data]) 

#     async def main(self):
#         server = await asyncio.start_server(
#             self._handler, self.IP, self.Port)
#         print('async 1')
#         async with server:
#             # await server.start_serving()
#             await server.serve_forever()
#         print('async 2')

#     def boo(self):
#          asyncio.Task(asyncio.run(self.main()))
        

# server = Server('127.0.0.1', 8888)
# server.boo()
# # asyncio.run(server.main())
# print('1')
# time.sleep(4)
# print('2')
# server.send_data('yes')


# 25/03/2023 22:59
# class AsyncServer():
#     def __init__(self, ip, port) -> None:
#         self.ip = ip
#         self.port = port
#         self._writer = None
#         self._outbound_queue = queue.SimpleQueue()
#         self.inbound_queue = queue.Queue()
#         self.clients_queue = []


#     def send_data(self, data):
#         self._outbound_queue.put(data)
        

#     def connected_clients(self):
#          temp = []
#          for item in self.clients_queue:
#               temp.append(item['addr'])
#          return  temp


#     def recived_messages(self):
#          return  list(self.inbound_queue.queue)


#     async def _handler(self, reader, writer):
#         self._writer = writer
#         addr = self._writer.get_extra_info('peername')
#         print(f"{addr!r} is connected.")
#         self.clients_queue.append({'addr' : addr, 'writer' : writer, 'reader' : reader})
#         pdb.set_trace()

#         try:
#             data = await reader.read(100)
#             message = data.decode()
#             self.inbound_queue.put(message)
#         except Exception as ex:
#             print(f'in _handler {type(ex)}, {ex}')


#     async def _send_data(self):
#             while(True):
#                 try:
#                     item = self._outbound_queue.get(block=False)
#                     self._writer.write(item.encode())
#                     await self._writer.drain()
#                     await asyncio.sleep(0.1)
#                 except queue.Empty:
#                      await asyncio.sleep(0.5)
#                      continue
#                 except ConnectionResetError:
#                     print('ConnectionResetError')
#                     await asyncio.sleep(0.1)
#                 except Exception as ex:
#                      print(type(ex), ex, 'Unhandeled')



#     async def _start_server(self):
#         server_coro = await asyncio.start_server(self._handler, self.ip, self.port)
#         async with server_coro:
#             await server_coro.serve_forever()



#     async def _main(self):
#         tasks = []
#         tasks.append(asyncio.create_task(self._start_server()))
#         tasks.append(asyncio.create_task(self._send_data()))

#         await asyncio.gather(*tasks)


#     def run(self):
#          asyncio.run(self._main())
