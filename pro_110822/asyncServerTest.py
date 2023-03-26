import asyncio
from multiprocessing.dummy import Pool
import time
# Listen for connections
# Accept connections and emmit to the mainwindow
# Send mouse and keyboard input
# Send managment data
# Recive managment data
# Connections monitor


class Server():
    def __init__(self, ip, port) -> None:
        self.IP = ip
        self.Port = port
        self._writer = None

    async def _handler(self, reader, writer):
        self._writer = writer
        data = await reader.read(100)
        message = data.decode()
        addr = self._writer.get_extra_info('peername')

        print(f"Received {message!r} from {addr!r}")

    async def _send_data(self, data):
            await asyncio.sleep(2)
            print(f"Send: {data!r}")
            self._writer.write(data.encode())
            await self._writer.drain()

    async def close_connection(self):
            print("Close the connection")
            self._writer.close()
            await self._writer.wait_closed()


    async def _start_server(self):
        server_coro = await asyncio.start_server(self._handler, self.IP, self.Port)
        async with server_coro:
            await server_coro.serve_forever()


    async def main(self):
        tasks = []
        tasks.append(asyncio.create_task(self._send_data("yes")))
        tasks.append(asyncio.create_task(self._start_server()))

        await asyncio.gather(*tasks)


    def boo(self):
         asyncio.run(self.main())
        

server = Server('127.0.0.1', 8888)
server.boo()

print('1')
time.sleep(4)
print('2')




























































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