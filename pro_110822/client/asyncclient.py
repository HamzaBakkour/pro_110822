import asyncio
import queue
import platform
from ctypes import windll

class AsyncClient():
    def __init__(self) -> None:
        self._reader = None
        self._writer = None
        self._inbound_queue = queue.Queue()
        self._outbound_queue = queue.SimpleQueue()
        self._recive_message_s1 = 0.1


    def addto_inbound_queue(self, data):
        if (data != '*'):
            self._inbound_queue.put(data)
            print(f"{data} added to self._inbound_queue")



    @staticmethod
    def _pack_data(data_, head_length = 7):
        head = str(len(data_.encode()))
        for _ in range(0, head_length - len(head)):
            head = head + '+'
        # packed_data = head + data_ + '++++'
        packed_data = head + data_ 
        return packed_data.encode()


    async def _connect(self, serverIP, serverPort):
        try:
            print(f"trying to connect to server {serverIP}:{serverPort}")
            self._reader, self._writer = await asyncio.open_connection(serverIP, serverPort)
            print("connected")
        except Exception as ex:
            print(f'asyncclient, _connect, {type(ex)}, {ex}')




    async def _recive_message(self):
        while(True):
            try:
                head_length = await self._reader.read(7)
            except AttributeError as ae:
                await asyncio.sleep(1)
                print(f'asyncclient, in _recive_message, {ae}, sleeping 1s')
                continue

            head_length = head_length.decode()
            head_length = head_length.replace('+', '')
            try:
                head_length = int(head_length)
            except ValueError:
                print(f'asyncclient, _recive_message, invaled head_length:{head_length}, passed.')
                continue
            data = await self._reader.read(head_length)
            data = data.decode()
            if data.startswith('$'):
                print("client message recived $$")
                await self._handel_server_messages(data)
            else:
                self.addto_inbound_queue(data)

            await asyncio.sleep(self._recive_message_s1)


    async def _handel_server_messages(self, message):
        match message:
            case '$INFO_R':
                await self._send_client_info_to_server()


    async def _send_client_info_to_server(self):
        name = self._get_pc_name()
        resulotion = self._get_screen_resulotion()
        await self._send_data(f'€INFO_R!{name}!{resulotion}')


    @staticmethod
    def _get_pc_name():
        return platform.node()
    

    @staticmethod
    def _get_screen_resulotion():
        user32 = windll.user32
        resulotion = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return resulotion



    async def _send_data(self, data):
        if (self._writer == None):
            return
        try:
            data = self._pack_data(data)
            print(f"asyncclient, _send_data, sending:{data}")
            self._writer.write(data)
            await self._writer.drain()
            print(f"asyncclient, _send_data, sending:{data}, complete")
        except ConnectionResetError:
            print('ConnectionResetError')
            await asyncio.sleep(0.1)
        except Exception as ex:
                print(type(ex), ex, 'Unhandeled')


    def recived_messages(self):
        return  list(self._inbound_queue.queue)
    



    async def _wait_on_connection_close(self):
        if (self._writer == None):
            return
        print("waiting on connection close")
        await self._writer.wait_closed()
        print("connection closed")


    async def _main(self, serverIP, serverPort):
        tasks = []
        tasks.append(asyncio.create_task(self._connect(serverIP, serverPort)))
        tasks.append(asyncio.create_task(self._recive_message()))

        await asyncio.gather(*tasks)



    def close_connection(self):
        try:
            self._writer.close()
            asyncio.run(self._wait_on_connection_close())
        except Exception as ex:
            print(type(ex))



    def connect(self, serverIP, serverPort):
         asyncio.run(self._main(serverIP, serverPort ))

        
            




































































































































































































































































    #26/03/2023 12:36
    # async def _recive_message(self):
    #     while(True):
    #         try:
    #             data = await self._reader.read(6)
    #             if (len(data) == 6):   
    #                 head = data.decode()
    #                 data_length = int(head.replace('+', ''))
    #                 data = await self._reader.read(data_length)
    #                 data = data.decode()
    #                 self.inbound_queue.put(data)
    #                 print(f"{data} added to self._inbound_queue")
    #             else:
    #                 await asyncio.sleep(0.1)
    #         except AttributeError as ae:
    #             print('in _recive_message ', ae, ' ', type(ae))
    #             await asyncio.sleep(1)
    #         except Exception as ex:
    #             print(type(ex), ex,' in _recive_message')
    #             await asyncio.sleep(1)













# async def tcp_echo_client(message):
#     reader, writer = await asyncio.open_connection('127.0.0.1', 8888)


#     while(True):
#         try:
#             data = await reader.read(100)
#             print(f'Received: {data.decode()!r}')
#             await asyncio.sleep(1)
#         except Exception as ex:
#             print(type(ex))
#             print('Close the connection')
#             try:
#                 writer.close()
#                 await writer.wait_closed()
#             except Exception as ex:
#                 print(type(ex))
#             break

# asyncio.run(tcp_echo_client('Hello World!'))



    # print(f'Send: {message!r}')
    # writer.write(message.encode())
    # await writer.drain()





# import asyncio

# async def tcp_echo_client(message):
#     reader, writer = await asyncio.open_connection(
#         '127.0.0.1', 8888)

#     print(f'Send: {message!r}')
#     writer.write(message.encode())
#     await writer.drain()

#     data = await reader.read(100)
#     print(f'Received: {data.decode()!r}')

#     print('Close the connection')
#     writer.close()
#     await writer.wait_closed()

# asyncio.run(tcp_echo_client('Hello World!'))