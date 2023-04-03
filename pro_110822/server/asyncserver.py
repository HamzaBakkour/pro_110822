import asyncio
from asyncio.exceptions import CancelledError
import queue
from server.senduserinput import SendUserInput
import pdb


class AsyncServer():
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port
        self.stream = False
        self.inbound_queue = queue.Queue(maxsize=100)
        self.clients_queue = []
        self._server_coro = None
        self._main_tasks_group = None
        self._writer = None
        self._reader = None
        self._capture_input = SendUserInput()
        self._send_data_s1_ = 1
        self._recive_data_task_s1 = 1
        self._connections_monitor_s1_ = 0.1
        self._connections_monitor_s2_ = 1
        self._start_stream_s1_ = 0.1
        self._start_stream_s2_ = 1

    @property
    def connected_clients(self):
         temp = []
         for item in self.clients_queue:
              temp.append((item['addr'], item['name'], item['rez']))
         return  temp

    @property
    def _connected_clients_all(self):
        return self.clients_queue

    @staticmethod
    def _pack_data(data_, head_length = 7):
        head = str(len(data_.encode()))
        for _ in range(0, head_length - len(head)):
            head = head + '+'
        # packed_data = head + data_ + '++++'
        packed_data = head + data_ 
        return packed_data.encode()


    ######## active client ########################################################       
    def set_active(self, clientIP, clientPort):
        temp = self._connected_clients_all
        for client in temp:
            if ((client['addr'][0] == clientIP) and (client['addr'][1] == clientPort)):
                self._reader =  client['reader']
                self._writer =  client['writer']
                print(f"\nasyncserver, {client['addr'][0]}:{client['addr'][1]} is now active")
                return
        print(f"\nasyncserver, could not fined client {clientIP}:{clientPort} in connected clients.")

    def send_data_to_active(self, data):
        data = self._pack_data(data)
        asyncio.run(self._send_data(data))

    async def _send_data(self, data):
            if (self._writer == None):
                print("\nasyncserver, no client was set. use set_client to set one.")
                return
            try:
                self._writer.write(data)
                await self._writer.drain()
            except ConnectionResetError:
                print('\nasyncserver, ConnectionResetError')
                await asyncio.sleep(self._send_data_s1_)
            except Exception as ex:
                    print('\nasyncserver, ', type(ex), ex, 'Unhandeled')

    def broadcast(self, message):
        was_active_r = self._reader
        was_active_w = self._writer

        for client in self.connected_clients:
            self.set_active(client[0], client[1])
            self.send_data_to_active(message)

        self._reader = was_active_r 
        self._writer = was_active_w 

    def start_stream(self):
        self._capture_input.start_listning()
        self.stream = True

    def stop_stream(self):
        self.stream = False
        self._capture_input.stop_listning()

    async def _start_stream(self):
        while(True):
            if (self.stream): 
                for _ in range(self._capture_input.events_queue.qsize()):
                    item = self._capture_input.events_queue.get()
                    await self._send_data(item)
                await asyncio.sleep(self._start_stream_s1_)
            else:
                await asyncio.sleep(self._start_stream_s2_)
  ################################################################   



   ######## all clients ########################################################    
    def recived_messages(self):
         return  list(self.inbound_queue.queue)

    def _add_to_inbound (self, data):
        if (len(data) > 0):
            print(f"\nasyncserver, added {data} to inbound queue")
            self.inbound_queue.put(data)

    async def _connections_monitor(self):
        while(True):
            connections = self._connected_clients_all
            for connection in connections:
                try:
                    message = self._pack_data('*')
                    connection['writer'].write(message)
                    await connection['writer'].drain()
                except Exception as ex:
                    print('\nasyncserver, in _connections_monitor, ',  connection['addr'], type(ex), ' ', ex, ' [CLOSED]')
                    try:
                        connection['writer'].close()
                        await connection['writer'].wait_closed()
                    except (ConnectionAbortedError, ConnectionResetError):
                        pass
                    except Exception as ex:
                        print('\nasyncserver, in _connections_monitor ', type(ex), ' ', ex)
                    connections.remove(connection)
                await asyncio.sleep(self._connections_monitor_s1_)
            await asyncio.sleep(self._connections_monitor_s2_)

    async def _async_send_data_on_writer(self, data, writer):
            if (writer == None):
                print("\nasyncserver, _send_data_on_writer, invalid writer")
                return
            data = self._pack_data(data)
            try:
                writer.write(data)
                await writer.drain()
            except ConnectionResetError:
                print('\nasyncserver, ConnectionResetError')
            except Exception as ex:
                    print('\nasyncserver, ', type(ex), ex, 'Unhandeled')     

    def _client_messages_handler(self, message):
        def extract_name_and_rez(message):
            str_to_list = message.split('!')
            name_ = str_to_list[1]
            resulotion_ = tuple((str_to_list[2], str_to_list[3]))
            ip_ = str_to_list[-2]
            port_ = str_to_list[-1]
            return name_, resulotion_, ip_, port_
        
        if message.startswith('€INFO_R'): # €INFO_R is a respond from the client to a
                                          # $INFO_R request that is sent by the server.
                                          # $INFO_R is a requst sent by the server to ask 
                                          # the client for its name and screen resulotion.
            name, resulotion, ip, port = extract_name_and_rez(message)
            clients = self._connected_clients_all
            for client in clients:
                if ((client['addr'][0] == ip) and (str(client['addr'][1]) == port)):
                    #update the client with the info that was recived.
                    client['name'] = name
                    client['rez'] = resulotion
                    print(f'\nasyncserver, _client_messages_handler, client:{client} ' \
                            f'was updated with name:{name} and resulotion:{resulotion} ' \
                            f'new client:{client}')
        else:
            self._add_to_inbound(message)

    async def _recive_data_task(self, connection):
        print(f'\nasycnserver, _recive_data_task, task was created with connection:{connection}')
        client_ip = connection['addr'][0]
        client_port = str(connection['addr'][1])
        while(True):
            try:
                head_length = await connection['reader'].readexactly(7)
                head_length = head_length.decode()
                head_length = head_length.replace('+', '')
                head_length = int(head_length)
                data = await connection['reader'].read(head_length)
                data = data.decode()
                print(f"\nasyncserver, _recive_data, data:{data}")
                self._client_messages_handler(data + '!' + client_ip + '!' + client_port)
                await asyncio.sleep(self._recive_data_task_s1)
            except ConnectionResetError as cr:
                print(f"\nasyncserver, _recive_data, {type(cr)}, {cr}, returning")
                return

    async def _schedule_recive_data_tasks(self, async_task_group):

        tracked_clients = []
        recive_data_tasks = []

        def in_list1_not_in_list2(list1, list2):
            result = []
            for i in list1:
                add = True
                for ii in list2:
                    if i == ii:
                        add = False
                if (add and i not in result):
                    result.append(i)
            return result

        def in_list2_not_in_list1(list1, list2):
            result = []
            for ii in list2:
                add = True
                for i in list1:
                    if ii == i:
                        add = False
                if (add and ii not in result):
                    result.append(ii)
            return result

        def tracked_clients_changed():
            changes = {'to_be_added' : [], 'to_be_removed' : []}
            connected = self._connected_clients_all
            #connected but not tracked -> added
            changes['to_be_added'] = in_list1_not_in_list2(connected, tracked_clients)
            #tracked but not connected -> removed
            changes['to_be_removed'] = in_list2_not_in_list1(connected, tracked_clients)
            if ((len(changes['to_be_added']) > 0) or (len(changes['to_be_removed']) > 0)):
                return changes
            return False
        
        async def close_connection(connection):
            try:
                connection.close()
                await connection.wait_closed()
            except (ConnectionAbortedError, ConnectionResetError) as ex:
                print(f'\nasyncserver, _schedule_recive_data_tasks, {type(ex)}, {ex} [OK]')
            except Exception as ex:
                print('\nasyncserver, in _connections_monitor ', type(ex), ' ', ex)

        async def reschedule_tasks(changes_):
            for change in changes_['to_be_added']:

                recive_data_tasks.append(async_task_group.create_task(self._recive_data_task(change)))

            await asyncio.sleep(1)

            for change in changes_['to_be_removed']:
                await close_connection(change['writer'])

        while(True):
            changes = tracked_clients_changed()
            if (not changes):
                await asyncio.sleep(1)
                continue
            print(f'\nasyncserver, _schedule_recive_data_tasks, changes:{changes}')
            for change in changes['to_be_added']:
                tracked_clients.append(change)
            for change in changes['to_be_removed']:
                tracked_clients.remove(change)
            print(f'\nasyncserver, _schedule_recive_data_tasks, tracked_clients:{tracked_clients}')
            await reschedule_tasks(changes)
    ################################################################


    ######## server ########################################################   
    async def _handler(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"\nasyncserver, {addr!r} is connected.")
        self._connected_clients_all.append({'addr' : addr,
                                   'writer' : writer,
                                   'reader' : reader,
                                   'name' : '',
                                   'rez' : '',
                                   'id' : ''})
        print("\nsending info request to client")
        await self._async_send_data_on_writer('$INFO_R', writer)
        print("\ninfo request sent")

    async def _start_server(self):
        self._server_coro = await asyncio.start_server(self._handler, self.ip, self.port)
        async with self._server_coro:
            try:
                print(f"\nasyncserver, starting server at {self.ip}:{self.port}")
                await self._server_coro.serve_forever()
            except CancelledError:
                print('\nasyncserver, server_coro apported', CancelledError)

    async def _main(self):
        main_tasks = []

        async with asyncio.TaskGroup() as tg:
            main_tasks.append(asyncio.create_task(self._start_server()))
            main_tasks.append(asyncio.create_task(self._schedule_recive_data_tasks(tg)))
            main_tasks.append(asyncio.create_task(self._connections_monitor()))
            main_tasks.append(asyncio.create_task(self._start_stream()))

            self._main_tasks_group = asyncio.gather(*main_tasks)
            try:
                await self._main_tasks_group
            except CancelledError:
                print('\nasyncserver, _main_tasks_group cancelled', CancelledError)
            print('\nasyncserver, _main() exited.')

    def run(self):
         asyncio.run(self._main())

    def close(self):
        succes = True
        if (self._server_coro != None):
            print("\nasyncserver, close, closing...")
            try:
                self._server_coro.close()
            except Exception as ex:
                succes = False
                print('\nin AsyncServer, close server coro, ' ,ex, type(ex), '[X]')

            try:
                asyncio.run(self._server_coro.wait_closed())
            except Exception as ex:
                succes = False
                print('\nin AsyncServer, close, ' ,ex, type(ex), '[X]')
            else:
                print("\nasyncserver, close, server closed. [OK]")

        if (self._main_tasks_group == None):
            return
        
        try:
            print("\nasyncserver, close, canceling tasks group...")
            self._main_tasks_group.cancel()
        except Exception as ex:
            succes = False
            print('\nin AsyncServer, close, server groups, ' ,ex, type(ex), '[X]')
        else:
            print("\nasyncserver, close, canceling tasks group, canceled. [OK]")


        if(succes):
            print("\nasyncserver, server closed SUCCESSFULLY [OK]")
        else:
            print("\nasyncserver, server closed with ERROR [X].")
    ################################################################
        



































#02/04/2023 09:29
# class TrackableList(list):
#     def __init__(self, iterable):
#         super().__init__(item for item in iterable)
#         self._NUM = 0
#         self._OLDNUM = 0
#     def __setitem__(self, index, item):
#         self._change_num()
#         super().__setitem__(index, item)
#     def append(self, item) -> None:
#         self._change_num()
#         super().append(item)
#     def remove(self, item) -> None:
#         self._change_num()
#         super().remove(item)
#     def _change_num(self):
#         if (self._NUM > 1000):
#             self._NUM = 0
#             self._OLDNUM = -1
#         else:
#             self._NUM = self._NUM + 1
#     def was_changed(self):
#         if (self._OLDNUM == self._NUM):
#             return False
#         else:
#             self._OLDNUM = self._NUM
#             return True



    #01/04/2023 17:47
    # async def _recive_data(self):
    #     while(True):
    #         connections = self._connected_clients_all
    #         print("*_recive_data, START")
    #         for connection in connections:
    #             print("*_recive_data, IN")
    #             # try:
    #             print(f"*asyncserver, _recive_data, from connection:{connection}")
    #             print("*_recive_data, 1")

    #             head_length = await connection['reader'].readexactly(7)
    #             # pdb.set_trace()
    #             print(f"*_recive_data, 2, head_length:{head_length}")
    #             # head_length = head_length.decode()
    #             # head_length = head_length.replace('+', '')
    #             # head_length = int(head_length)
    #             # data = await connection['reader'].read(head_length)
    #             # data = data.decode()
    #             # print(f"asyncserver, _recive_data, data:{data}")
    #             # self._add_to_inbound(data)
    #             # except Exception as ex:
    #                 # print(f'asyncserver, in _recive_data {type(ex)}, {ex}')
    #             await asyncio.sleep(self._recive_data_s1_)
    #         await asyncio.sleep(self._recive_data_s2_)
    #     print('_recive_data, exiting')



          # except Exception as ex:
                # print(f'asyncserver, in _recive_data {type(ex)}, {ex}')
        # await asyncio.sleep(self._recive_data_s2_)
        # print('_recive_data, exiting')



        # def tracked_clients_changed():
        #     temp_list = self._connected_clients_all
        #     for client in temp_list:
        #         if (client not in self._tracked_clients):
        #             self._tracked_clients.append(client)
        #     for client in self._tracked_clients:
        #         if (client not in temp_list):
        #             self._tracked_clients.remove(client)
        #     if (self._tracked_clients.was_changed()):
        #         return True
        #     return False



        #31/03/2023 17:40
        # while(True):
        #     connections = self._connected_clients_all()
        #     for connection in connections:
        #         try:
        #             print('start')
        #             head = await connection['reader'].read(7)
        #             print(f'1, head: {head}')
        #             head = head.decode()
        #             print(f'2, head.decode(): {head}')
        #             head = head.replace('+', '')
        #             print(f'3, head: {head}')
        #             head_length = int(head)
        #             print(f'4, head_length: {head_length}')
        #             data = await connection['reader'].read(head_length)
        #             print(f'5, data: {data}')
        #             data = data.replace('+', '')
        #             print(f'6, data: {data}')
        #             print(f"asyncserver, _recive_data, data:{data}")
        #             self._add_to_inbound(data)
        #         except Exception as ex:
        #             print(f'asyncserver, in _recive_data {type(ex)}, {ex}')
        #         await asyncio.sleep(self._recive_data_s1_)
        #     await asyncio.sleep(self._recive_data_s2_)

        # while(True):
        #     connections = self._connected_clients_all()
        #     for connection in connections:
        #         try:
        #             data = await connection['reader'].read(4)
        #             message = data.decode()
        #             self._add_to_inbound(message)
        #         except Exception as ex:
        #             print(f'asyncserver, in _recive_data {type(ex)}, {ex}')
        #         await asyncio.sleep(self._recive_data_s1_)
        #     await asyncio.sleep(self._recive_data_s2_)



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