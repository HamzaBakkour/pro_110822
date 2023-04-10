from asyncio.exceptions import CancelledError
from PySide6.QtCore import QRunnable, Slot, QObject, Signal, QTimer, SIGNAL
from typing import Optional
import time
from server.asyncserver import AsyncServer
from prologging import Log

# Server emmit signal to main window every 1s
# -> Server needs a slot that the clien can connect to
# -> Server will emmit
# -> Server needs a timer which tick every 1s
#
#
#



class Server(QRunnable):
    def __init__(self, serverIP, serverPort) -> None:
        super(Server, self).__init__()
        self.ip = serverIP
        self.port = serverPort
        self._server = AsyncServer(self.ip, self.port)
        self.alive = True
        self.timer = None
        self._log = Log()

    @property
    def connected_clients(self):
        return self._server.connected_clients
    

    @property
    def recived_messages(self):
        return self._server.recived_messages()

    def set_client(self, clientIP, clientPort):
        self._server.set_active(clientIP, clientPort)

    def send_data(self, data):
        self._server.send_data_to_active(data)

    def broadcast(self, message):
        self._server.broadcast(message)


    def stream_to_client(self):
        self._server.start_stream()

    def stop_stream(self):
        self._server.stop_stream()

    def close_server(self):
        self._server.close()


    @Slot()
    def run(self)-> None:
        try:
            self._log.info(['run'],
                           message='STARTING the server...')
            # print('server, run, STARTING the server...')
            self._server.start()
            self._log.info(['run'],
                           message='server STOPPED')
            # print('server, run, server STOPED...')
        except CancelledError:
            self._log.error(['run'],
                      message=f'server was canceled {CancelledError}, returning...')
            # print(f'\nserver, server was canceled {CancelledError}, returning...')
            return


class SSignals(QObject):
     server_view_maneger = Signal()
     recived_messages = Signal()

class ServerSignals(QRunnable):
    def __init__(self) -> None:
        super(ServerSignals, self).__init__()
        self.signals = SSignals()
        self.alive = True
        self.tick = 1
    @Slot()
    def run(self) -> None:
        while(self.alive):
            self.signals.server_view_maneger.emit()
            self.signals.recived_messages.emit()
            time.sleep(self.tick)






# server = Server('127.0.0.1', 8888)
# threabool = QThreadPool()
# threabool.setMaxThreadCount(25)
# threabool.start(server)
# print('')
# server.close_server()
# connected = server.connected_clients()
# server.set_client(connected[0][0], connected[0][1])
# print('')
# print('stream started')
# server.start_stream()
# print('')
# print('stream stoped')
# server.stop_stream()
#[len data + 3]
#[++++++]     [data][+++]
# for _ in range(100):
#     server.send_data("29++++12345!6789AB!CDEFGH!IJKLM!+++")
# server.send_data("19++++yes from server1+++")
# server.send_data("18++++no from server1+++")
# connected = server.connected_clients()
# server.stream_to_client(connected[1][0], connected[1][1])
# server.send_data("19++++yes from server2+++")
# server.send_data("18++++no from server1+++")
# connected_clients = server.connected_clients()
# recived_messages = server.recived_messages()
# print("ended")




































































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