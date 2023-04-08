import asyncio
from asyncio.exceptions import CancelledError
import queue
import platform
import pdb
from ctypes import windll


class TasksAborted(Exception):
    pass


class AsyncClient():
    def __init__(self) -> None:
        self._reader = None
        self._writer = None
        # self._serverIP = None
        # self._serverPort = None
        self._connected = False
        self._abort_tasks = False
        self._exit = False
        self._resume = True
        self._tasks = []
        self._inbound_queue = queue.Queue()
        self._outbound_queue = queue.SimpleQueue()
        self._recive_message_s1 = 0.1
    
    def is_connected(self):
        if (self._reader == None) and (self._writer == None):
            return False
        return True

    def _inbound_queue_put(self, data):
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
            print(f"\nasyncclient, _connect, trying to connect to server {serverIP}:{serverPort}")
            self._reader, self._writer = await asyncio.open_connection(serverIP, serverPort)
            self._serverIP = serverIP
            self._serverPort = serverPort
            self._connected = True
            print("\nasyncclient, _connect, connected")
        except Exception as ex:
            print(f'asyncclient, _connect, {type(ex)}, {ex}')

    async def _recive_message(self):
        failed = 0
        sleep_ = 0.3
        allowed_failures = 20 
        while (True):
            if not self._connected:
                print('asyncclient, in _recive_message, client is not connected to the server yet,'\
                      f'\ncannot start reciving message task, cheking again in {sleep_} seconds...')
                await asyncio.sleep(sleep_)
                failed += 1
                if failed > allowed_failures:
                    print(f"\nasyncclient, _recive_message, waited for {failed*sleep_}s"\
                          "\nasyncclient, client still not connected -> RASING EXEPTION, EXITING...")
                    raise TasksAborted
            else:
                print('\nasyncclient, cliens is now connected, STARTING recive message task')
                break

        # failed = 0

        while(True):
            try:
                head_length = await self._reader.read(7)
            # except AttributeError:
            #     print('\nasyncclient, in _recive_message, AttributeError, -> sleeping 0.1s + continue [OK]')
            #     await asyncio.sleep(0.1)
            #     failed += 1
            #     if failed > 50:
            #         print('\nasyncclient, in _recive_message, reached max failed allowed RAISING EXEPTION')
            #         raise TasksAborted
            #     continue
            except Exception as ex:
                print(f'\nasyncclient, in _recive_message, head_length {type(ex)}, {ex}, RAISING EXEPTION -> TERMINATING...')
                raise TasksAborted


            try:
                head_length = head_length.decode()
                head_length = head_length.replace('+', '')
                head_length = int(head_length)
            # except ValueError:
            #     print(f'asyncclient, _recive_message, invaled head_length:{head_length}, sleeping 0.1s + continue [OK].')
            #     await asyncio.sleep(0.1)
            #     failed += 1
            #     if failed > 50:
            #         print('\nasyncclient, in _recive_message, reached max failed allowed RAISING EXEPTION')
            #         raise TasksAborted
            #     continue
            except Exception as ex:
                print(f'\nasyncclient, in _recive_message, head_length2 {ex}, {type(ex)}, RAISING EXPETION')
                raise TasksAborted

            
            try:
                data = await self._reader.read(head_length)
                data = data.decode()
            # except AttributeError:
            #     await asyncio.sleep(0.1)
            #     failed += 1
            #     if failed > 50:
            #         print('\nasyncclient, in _recive_message, data, reached max failed allowed RAISING EXEPTION')
            #         raise TasksAborted
            #     continue
            except Exception as ex:
                print(f'\nasyncclient, in _recive_message, data {ex}, {type(ex)}, RAISING EXPETION')
                raise TasksAborted
            if data.startswith('$'):
                print("client message recived $$")
                await self._handel_server_messages(data)
            else:
                self._inbound_queue_put(data)

            # failed = 0
            
            await asyncio.sleep(self._recive_message_s1)

    async def _group_tasks_terminator(self, sleep_ = 1):
        while(True):
            if self._abort_tasks or self._exit:
                print("\nasyncclient, _group_tasks_terminator, raising TasksAborted...")
                self._abort_tasks = False
                self._resume = False
                raise TasksAborted
            await asyncio.sleep(sleep_)

    def re_open_connection(self):
        if not self._resume:
            self._resume = True
        else:
            print('\nasyncclient, re_open_connection called, _resume is True, [X]')

    def close_connection(self):
        self._abort_tasks = True

    async def _handel_server_messages(self, message):
        match message:
            case '$INFO_R':
                await self._send_client_info_to_server()

    async def _send_client_info_to_server(self):
        name = self._get_pc_name()
        resulotion = self._get_screen_resulotion()
        await self._send_data(f'€INFO_R!{name}!{resulotion[0]}!{resulotion[1]}')

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
            print('\nasyncclient, in _send_data, trying to send data on a None writer -> RETURNING.')
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

    async def _main(self, serverIP, serverPort):

        while(True):
            if self._exit:
                return
            if not self._resume:
                # print('\nasyncclient, _main, _resum is false -> sleeping for 0.1s')
                await asyncio.sleep(1)
                continue

            self._tasks.append(asyncio.create_task(self._connect(serverIP, serverPort)))
            self._tasks.append(asyncio.create_task(self._recive_message()))
            self._tasks.append(asyncio.create_task(self._group_tasks_terminator()))


            done, pending = await asyncio.wait(self._tasks , return_when=asyncio.FIRST_EXCEPTION)

            for task in done:
                print(f'\nasyncserver, _main, done tasks:{task}')
            for task in pending:
                print(f'\nasyncserver, _main, pending tasks:{task}')

            await self._close_connection()

            # tasks = asyncio.all_tasks()
            for task in  self._tasks:
                # pdb.set_trace()
                try:
                    # if task.get_coro().__name__ != '_main':
                    print(f'\nCANCELING>>> task:{task}')
                    task.cancel()
                    self._tasks.remove(task)
                    print(f'\ntask:{task.get_name()} <<<CANCELED')
                except Exception as ex:
                    print(f'\nasyncserver, _main, task.cancel(), {type(ex)}, {ex}')

            # for task in 

            print(f'\nasyncclient, _main, at END, asyncio.all_tasks:{asyncio.all_tasks()}')
            print(f'\nasyncclient, _main, at END, self._tasks:{self._tasks}')
            await asyncio.sleep(1)

            # pdb.set_trace()

#run _main in a while loop
#when self._abort_tasks is set to true in the task _group_tasks_terminator 
#   _group_tasks_terminator will raise an exeption, 
#   the asyncio.wait will return
#   the connection will be terminated
#   and the tasks will be canceled

#here we have two variable (false from the begning)
# self._exit and self._resume

#if self._exit is false and self._resume is false -> sleep for 0.1s
#if self._exit is false and self._resume is true -> continue + set self._resum to false
#if self._exit is true, return



    async def _close_connection(self):
        try:
            self._writer.close()
            await self._writer.wait_closed()
        except (ConnectionAbortedError, ConnectionResetError) as ex:
            print(f'\nasyncclient, _close_connection, {type(ex)}, {ex} [OK]')
        except Exception as ex:
            print('\nasyncclient, _close_connection ', type(ex), ' ', ex)
            return
        self._writer = None
        self._reader = None
        print('\nasyncclient, _close_connection connection CLOSED.')


    async def _wait_on_connection_close(self):
        if (self._writer == None):
            return
        print("waiting on connection close")
        await self._writer.wait_closed()
        self._writer = None
        self._reader = None
        self._connected = False
        print("connection closed")

    def connect(self, serverIP, serverPort):

        try:
            asyncio.run(self._main(serverIP, serverPort))
        except CancelledError:
            print('asyncclient, connect, asyncio.run catched CancelledError -> EXITING')

        
            





        # try:
        #     self._writer.close()
        #     asyncio.run(self._wait_on_connection_close())
        # except Exception as ex:
        #     print(type(ex))


#init the client class without any input

#call the method connect with ip and port
# -> start the connect tasks + recive message task

#dissconnect -> end the tasks and close the connection
#reconnect   -> reopen the connection


    # def close_connection_perm(self):
    #     print(' ')

    # def close_connection_temp(self):
    #     if (self._reader == None) or (self._writer == None):
    #         print(f'\nasyncclient in close_connection_temp reader:{self._reader} or writer:{self._writer}'\
    #               'nis allready None, cannot pause connection -> RETURNING')
    #         return
    #     self._reader_save = self._reader 
    #     self._writer_save = self._writer
    #     self._reader = None
    #     self._writer = None

    # def reopen_connection(self):
    #     if (self._reader != None) and (self._writer != None):
    #         print(f'\nasyncclient in reopen_connection reader:{self._reader} and writer:{self._writer}'\
    #               'nare not None, cannot reopen connection -> RETURNING')
    #         return
    #     self._reader = self._reader_save
    #     self._writer = self._writer_save      
    #     self._reader_save = None
    #     self._writer_save = None




                #  if (self._abort_tasks):
                #     print('\nasyncclient, in _recive_message, raising TasksAborted -> RETURNING...')
                #     raise TasksAborted



















































































































































































































































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