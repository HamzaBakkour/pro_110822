import asyncio
import queue

class AsyncClient():
    def __init__(self) -> None:
        self._reader = None
        self._writer = None
        self._inbound_queue = queue.Queue()
        self._outbound_queue = queue.SimpleQueue()



    def send_data(self, data):
        asyncio.run(self._send_data(data))


    def addto_inbound_queue(self, data):
        if (data != '*'):
            self._inbound_queue.put(data)
            print(f"{data} added to self._inbound_queue")


    async def _send_data(self, data):
        if (self._writer == None):
            return
        try:
            self._writer.write(data.encode())
            await self._writer.drain()
        except ConnectionResetError:
            print('ConnectionResetError')
            await asyncio.sleep(0.1)
        except Exception as ex:
                print(type(ex), ex, 'Unhandeled')



    async def _connect(self, serverIP, serverPort):
        self._reader, self._writer = await asyncio.open_connection(serverIP, serverPort)



    async def _recive_message(self):
        await asyncio.sleep(1)
        while(True):
                try:
                    data = await self._reader.read(50)
                    data = data.decode()
                    self.addto_inbound_queue(data)
                except AttributeError as ae:
                    print('in _recive_message ', ae, ' ', type(ae))
                    await asyncio.sleep(1)
                except Exception as ex:
                    print(type(ex), ex,' in _recive_message')
                    await asyncio.sleep(1)



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