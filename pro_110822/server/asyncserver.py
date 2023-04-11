import asyncio
from asyncio.exceptions import CancelledError
import queue
from server.senduserinput import SendUserInput
from server.shortcuthandle import ShortcutsHandle
from prologging import Log
import pdb

class TasksAborted(Exception):
    pass

class AsyncServer():
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port
        self.stream = False
        self.inbound_queue = queue.Queue(maxsize=100)
        self.clients_queue = []
        self._tasks = []
        self._abort_tasks = False
        self._writer = None
        self._reader = None
        self._capture_input = SendUserInput()
        self._shortcut = ShortcutsHandle(self)
        self._shortcut.define_shortcut(('<ctrl>+m+1', 
                                                '_shortcut_handler'), 
                                               addToExist=False, 
                                               passShortcut=True)
        self._log = Log()
        self._id_list = []
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
              temp.append(((item['ip'], item['port']), item['name'], item['rez']))
         return  temp
    @property
    def _connected_clients_all(self):
        return self.clients_queue
    @staticmethod
    def _pack_data(data_):
        return f'{data_}&'.encode()

    def noo(self):
        print('noo')

    ######## active client ########################################################       
    def set_active(self, clientIP, clientPort):
        temp = self._connected_clients_all
        for client in temp:
            if ((client['ip'] == clientIP) and (client['port'] == clientPort)):
                self._reader =  client['reader']
                self._writer =  client['writer']
                self._log.info(['set_active'],
                            message=f"{client['ip']}:{client['port']} is now active")
                # print(f"\nasyncserver, {client['ip']}:{client['port']} is now active")
                return
        self._log.info(['set_active'],
                    message=f'could not fined client {clientIP}:{clientPort} in connected clients.')
        # print(f"\nasyncserver, could not fined client {clientIP}:{clientPort} in connected clients.")

    def send_data_to_active(self, data):
        data = self._pack_data(data)
        asyncio.run(self._send_data(data))

    async def _send_data(self, data):
            if (self._writer == None):
                self._log.error(['_send_data'],
                             message='no client was set. use set_client to set one.')
                # print("\nasyncserver, no client was set. use set_client to set one.")
                return
            try:
                self._writer.write(data)
                await self._writer.drain()
            except ConnectionResetError:
                self._log.error(['_send_data'],
                             message='ConnectionResetError')
                # print('\nasyncserver, _send_data, ConnectionResetError')
                await asyncio.sleep(self._send_data_s1_)
            except Exception as ex:
                    self._log.critical(['_send_data'],
                                    message=f'{type(ex)}, {ex}, Unhandeled')
                    # print('\nasyncserver, _send_data, ', type(ex), ex, 'Unhandeled')

    def is_streaming(self):
        return self.stream

    def start_stream(self):
        self._capture_input.supress_user_input()
        self._capture_input.start_listning()
        self.stream = True

    def stop_stream(self):
        self._capture_input.unsupress_user_input()
        self.stream = False
        self._capture_input.stop_listning()

    async def _start_stream(self):
        while(True):
            if (self.stream): 
                for _ in range(self._capture_input.events_queue.qsize()):
                    item = self._capture_input.events_queue.get()
                    await self._send_data(item.encode())
                await asyncio.sleep(self._start_stream_s1_)
            else:
                await asyncio.sleep(self._start_stream_s2_)
  ################################################################   



   ######## all clients ########################################################    
    def recived_messages(self):
         return  list(self.inbound_queue.queue)

    def broadcast(self, message):
        was_active_r = self._reader
        was_active_w = self._writer

        for client in self.connected_clients:
            self.set_active(client[0], client[1])
            self.send_data_to_active(message)

        self._reader = was_active_r 
        self._writer = was_active_w 

    def _add_to_inbound (self, data):
        if (len(data) > 0):
            self._log.info(['_add_to_inbound'],
                        message=f'added {data} to inbound queue')
            # print(f"\nasyncserver, added {data} to inbound queue")
            self.inbound_queue.put(data)

    async def _async_send_data_on_writer(self, data, writer):
            if (writer == None):
                self._log.error(['_async_send_data_on_writer'],
                             message='invalid writer')
                # print("\nasyncserver, _send_data_on_writer, invalid writer")
                return
            data = self._pack_data(data)
            try:
                self._log.info(['_async_send_data_on_writer'],
                            message=f'sending: {data} on writer: {writer}')
                # print(f"\nasyncserver, _send_data_on_writer, sending: {data} on writer: {writer}")
                writer.write(data)
                await writer.drain()
            # except ConnectionResetError:
            #     print('\nasyncserver, _async_send_data_on_writer, ConnectionResetError')
            except Exception as ex:
                    self._log.critical(['_async_send_data_on_writer'],
                                    message=f'{type(ex)}, {ex}, Unhandeled')
                    # print('\nasyncserver, _async_send_data_on_writer, ', type(ex), ex, ' Unhandeled')     

    def _client_info_respond(self, respond, client_ip, client_port):
        def extract_name_and_rez(message):
            str_to_list = message.split('!')
            name_ = str_to_list[1]
            resulotion_ = tuple((str_to_list[2], str_to_list[3]))
            return name_, resulotion_
        

        def defin_ctrl_m_id_shortcut(id_):
            self._log.info(['_client_info_respond', 'defin_ctrl_m_id_shortcut'],
                        message=f'called with id:{id_}')
            # print(f"\nasyncserver, _defin_ctrl_m_id_shortcut, called with id:{id_}'")
            shortcut_ = '<ctrl>+m+'+str(id_)
            target_function_ = '_shortcut_handler'
            self._shortcut.define_shortcut((shortcut_, target_function_))
            self._log.info(['_client_info_respond', 'defin_ctrl_m_id_shortcut'],
                        message=f"defined shortcut: '<ctrl>+m+{str(id_)}'")
            # print(f"\nasyncserver, _defin_ctrl_m_id_shortcut, defined shortcut: '<ctrl>+m+{str(id_)}'")
            return shortcut_, target_function_
        


        name, resulotion = extract_name_and_rez(respond)
        clients = self._connected_clients_all
        for client in clients:
            if ((client['ip'] == client_ip) and (str(client['port']) == client_port)):
                #give the client a shortcut passed on its id
                shortcut, target_function = defin_ctrl_m_id_shortcut(client['id'])
                client['shortcut'] = shortcut
                client['targe_function'] = target_function
                #update the client with the info that was recived.
                client['name'] = name

                client['rez'] = resulotion

                self._log.info(['_client_info_respond'],
                            message=f'client{client_ip}:{client_port} was updated with {name} {shortcut} {target_function} {resulotion}')
                # print(f'\nasyncserver, _client_info_respond, client{client_ip}:{client_port} was updated with {name} {shortcut} {target_function} {resulotion}')

    def _buffer_extractor(self, buffer_, client_ip, client_port):
        self._log.info(['_buffer_extractor'],
                    message=f'called with buffer: {buffer_}, {client_ip}, {client_port}')
        # print(f'\nasyncserver, _buffer_extractor, called with buffer: {buffer_}, {client_ip}, {client_port}')
        extracted_data = buffer_.split('&')

        for data in extracted_data:
            if data.startswith('€INFO_R'):
                self._client_info_respond(data, client_ip, client_port)
                # self._mouse_and_keyboard_controller(data)
            else:
                self._log.error(['_buffer_extractor'],
                             message=f'unknown data: {data}')
            # elif data.startswith('*'):
            #     self.l.debug(['_buffer_extractor'],
            #                  message='monitor')
            #     print(f'monitor>>> {data}')

    async def _recive_data_task(self, connection):
        self._log.info(['_recive_data_task'],
                    message=f'task was created with connection:{connection}')
        # print(f'\nasycnserver, _recive_data_task, task was created with connection:{connection}')
        client_ip = connection['ip']
        client_port = str(connection['port'])
        failed = 0
        while(True):
            try:
                buffer_ = b''
                while(buffer_[-1:] != b'&'):
                    data = await connection['reader'].read(1024)
                    if not data:
                        self._log.error(['_recive_data_task'],
                                     message='not data -> RAISING ValueError')
                        # print('\nasyncserver. _recive_data_task, not data -> FAILED')
                        raise ValueError
                    else:
                        buffer_ = buffer_ + data
                self._log.info(['_recive_data_task'],
                            message=f'client_ip:{client_ip}, client_port:{client_port} ' \
                                f'sending to buffer_extractor\nbuffer: {buffer_.decode()}')
                # print(f'\nasyncserver, _recive_data_task, client_ip:{client_ip}, client_port:{client_port}'\
                #     f"\nasyncserver, sending to buffer_extractor, buffer: {buffer_.decode()}")
                

                self._buffer_extractor(buffer_.decode(),  client_ip, client_port)

                failed = 0

            except (AttributeError, ValueError) as ex:
                self._log.error(['_recive_data_task'],
                              message=f'{type(ex)}, -> sleeping 0.1s + continue...')
                # print(f'\nasyncclient, in _recive_data_task, {type(ex)}, -> sleeping 0.1s + continue [OK]')
                await asyncio.sleep(0.1)
                failed += 1
                if failed > 10:
                    self._log.error(['_recive_data_task'],
                                 message='reached max failed allowed RETURNING...')
                    # print('\nasyncclient, in _recive_data_task, reached max failed allowed RAISING EXEPTION')
                    # raise TasksAborted
                    return
                continue
            except Exception as ex:
                self._log.critical(['_recive_data_task'],
                                message=f'{type(ex)}, {ex}, RETURNING, [UNHANDELED]')
                # print(f'\nasyncclient, in _recive_data_task, {type(ex)}, {ex}, RAISING EXEPTION -> TERMINATING...')
                # raise ex
                return

    async def _schedule_recive_data_tasks(self):

        tracked_clients = []

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
                self._log.info(['_schedule_recive_data_tasks',
                             'close_connection'],
                            message=f'{type(ex)}, {ex} [OK]')
                # print(f'\nasyncserver, _schedule_recive_data_tasks, {type(ex)}, {ex} [OK]')
            except Exception as ex:
                self._log.critical(['_schedule_recive_data_tasks',
                                 'close_connection'],
                                message=f'{type(ex)}, {ex} [UNHANDELED]')
                # print('\nasyncserver, in _connections_monitor ', type(ex), ' ', ex)

        async def reschedule_tasks(changes_):
            for change in changes_['to_be_added']:
                self._tasks.append(asyncio.create_task(self._recive_data_task(change)))
                self._log.info(['_schedule_recive_data_tasks',
                             'reschedule_tasks'],
                             message='ADDING +++')
                # print('\nasyncserver, _schedule_recive_data_tasks, reschedule_tasks, ADDING +++')
                for task in changes_['to_be_added']:
                    self._log.info(['_schedule_recive_data_tasks',
                                 'reschedule_tasks'],
                                 message=f'task:{task} [+++]')
                    # print(f'\nasyncserver, _schedule_recive_data_tasks, reschedule_tasks, task:{task} [+++]')

            await asyncio.sleep(1)

            for change in changes_['to_be_removed']:
                await close_connection(change['writer'])
                for task in self._tasks:
                    if task.done():
                        self._tasks.remove(task)
                        self._log.info(['_schedule_recive_data_tasks',
                                     'reschedule_tasks'],
                                     message=f'task:{task}, REMOVED')
                        # print(f'\nasyncserver, _schedule_recive_data_tasks, reschedule_tasks, task:{task}, REMOVED')

                # print('\nasyncserver, _schedule_recive_data_tasks, reschedule_tasks, REMOVING ---')
                self._log.info(['_schedule_recive_data_tasks',
                             'reschedule_tasks'],
                             message='REMOVING ---')
                
                for task in changes_['to_be_removed']:
                    self._log.info(['_schedule_recive_data_tasks',
                                 'reschedule_tasks'],
                                 message=f'task:{task} [---]')
                    # print(f'\nasyncserver, _schedule_recive_data_tasks, reschedule_tasks, task:{task} [---]')

        while(True):
            changes = tracked_clients_changed()
            if (self._abort_tasks):
                for client in self._connected_clients_all:
                    await close_connection(client['writer'])
                raise TasksAborted
            
            if (not changes):
                await asyncio.sleep(1)
                continue
            for change in changes['to_be_added']:
                tracked_clients.append(change)
            for change in changes['to_be_removed']:
                tracked_clients.remove(change)
            await reschedule_tasks(changes)
    ################################################################


    ######## server ########################################################
    def _get_id(self):
        for i in range(2,9):
            if i not in self._id_list:
                self._id_list.append(i)
                return i
        return False

    async def _connections_monitor(self):
        while(True):
            connections = self._connected_clients_all
            for connection in connections:
                try:
                    message = self._pack_data('*')
                    connection['writer'].write(message)
                    await connection['writer'].drain()
                except Exception as ex:
                    self._log.error(['_connections_monitor'],
                                 message=f"({connection['ip']}, {connection['port']}), {type(ex)}, {ex}, [CLOSING CONNECTION]")
                    # print('\nasyncserver, in _connections_monitor, ',  (connection['ip'], connection['port']), type(ex), ' ', ex, ' [CLOSING CONNECTION]')
                    self._id_list.remove(connection['id'])
                    self._log.info(['_connections_monitor'],
                                message=f"removing shortcut: <ctr>+m+{str(connection['id'])}")
                    # print("\nasyncserver, in _connections_monitor removing shortcut:", f"<ctr>+m+{str(connection['id'])}")
                    was_removed = self._shortcut.remove_shortcut(f"<ctrl>+m+{str(connection['id'])}")
                    if was_removed:
                        self._log.info(['_connections_monitor'],
                                    message=f"removing shortcut: <ctr>+m+{str(connection['id'])}, REMOVED")
                        # print("\nasyncserver, in _connections_monitor removing shortcut:", f"<ctr>+m+{str(connection['id'])}, REMOVED")
                    else:
                        self._log.info(['_connections_monitor'],
                                    message=f"removing shortcut: <ctr>+m+{str(connection['id'])}, WAS NOT REMOVED")
                        # print("\nasyncserver, in _connections_monitor removing shortcut:", f"<ctr>+m+{str(connection['id'])}, WAS NOT REMOVED")

                    try:
                        connection['writer'].close()
                        await connection['writer'].wait_closed()
                    except (ConnectionAbortedError, ConnectionResetError):
                        self._log.error(['_connections_monitor'],
                                     message='ConnectionAbortedError or ConnectionResetError ->' \
                                        'setting self._writer, self._reader to None if equal connection, STANDBY...')
                        
                        # print("\nasyncserver, in _connections_monitor ConnectionAbortedError or ConnectionResetError ->"\
                        #       "\nasyncserver, in _connections_monitor, setting self._writer, self._reader to None if equal connection, STANDBY...")
                        if (self._writer == connection['writer']) or (self._reader == connection['reader']):
                            self._writer = None
                            self._reader = None
                            if self.is_streaming():
                                self.stop_stream()
                                self._log.info(['_connections_monitor'],
                                            message='self._writer, self._reader is SET TO NONE + STOPPED STREAM')
                                # print("\nasyncserver, in _connections_monitor, self._writer, self._reader is SET TO NONE + STOPPED STREAM")
                            else:
                                self._log.info(['_connections_monitor'],
                                            message='self._writer, self._reader is NOT SET TO NONE')
                                # print("\nasyncserver, in _connections_monitor, setting self._writer, self._reader is SET NOT TO NONE")
                        else:
                            self._log.info(['_connections_monitor'],
                                        message='ConnectionAbortedError or ConnectionResetError, self._writer self._reader NOT SET TO None')
                            # print("\nasyncserver, in _connections_monitor ConnectionAbortedError or ConnectionResetError, self._writer self._reader NOT SET TO None")
                            


                    except Exception as ex:
                        self._log.critical(['_connections_monitor'],
                                        message=f'{type(ex)}, {ex}')
                        # print('\nasyncserver, in _connections_monitor ', type(ex), ' ', ex)
                    connections.remove(connection)
                await asyncio.sleep(self._connections_monitor_s1_)
            await asyncio.sleep(self._connections_monitor_s2_)

    def _shortcut_handler(self, shortcut):
        self._log.info(['_shortcut_handler'],
                    message=f'called with shortcut:{shortcut}')
        if shortcut == '<ctrl>+m+1':
            self.stop_stream()
            return
        clients = self._connected_clients_all
        for client in clients:
            if client['shortcut'] == shortcut:
                if self.is_streaming():
                    self.stop_stream()
                    self.set_active(client['ip'], client['port'])
                    self.start_stream()
                else:
                    self.set_active(client['ip'], client['port'])
                    self.start_stream()

    async def _server_handler(self, reader, writer):
        if self._abort_tasks:
            return
        addr = writer.get_extra_info('peername')
        self._log.info(['_server_handler'],
                    message=f'{addr!r} is connected.')
        # print(f"\nasyncserver, _server_handler, {addr!r} is connected.")

        id_ = self._get_id()
        if not id_:
            self._log.critical(['_server_handler'],
                            message='all IDs 2->9 are in use, RETURNING...')
            # print('\nasyncserver, _handler, all IDs 2->9 are in use, RETURNING...')
            raise TasksAborted


        self._connected_clients_all.append({'ip' : addr[0],
                                    'port' : addr[1],
                                   'writer' : writer,
                                   'reader' : reader,
                                   'name' : '',
                                   'rez' : '',
                                   'id' : id_,
                                   'shortcut' : '',
                                   'targe_function' : ''})
        self._log.info(['_server_handler'],
                    message='sending info request to client')
        # print("\nasyncserver, _handler, sending info request to client")
        await self._async_send_data_on_writer('$INFO_R', writer)
        # print("\nasyncserver, _handler, info request sent")
        self._log.info(['_server_handler'],
                    message='info request sent')

    async def _start_server(self):
        self._log.info(['_start_server'],
                    message='creating server coro...')
        # print('\nasyncserver, _start_server, creating server coro...')
        self._server_coro = await asyncio.start_server(self._server_handler, self.ip, self.port)
        self._log.info(['_start_server'],
                    message=f'creating server coro, DONE, {self._server_handler}, {self.ip}, {self.port}')
        # print(f'\nasyncserver, _start_server, creating server coro, DONE, {self._server_handler}, {self.ip}, {self.port}')
        async with self._server_coro:
            try:
                self._log.info(['_start_server'],
                            message=f'starting server at {self.ip}:{self.port}')
                # print(f"\nasyncserver, starting server at {self.ip}:{self.port}")
                await self._server_coro.serve_forever()
            except CancelledError:
                self._log.error(['_start_server'],
                             message='server_coro aborted, CancelledError')
                # print('\nasyncserver, server_coro aborted, CancelledError')
            except Exception as ex:
                self._log.critical(['_start_server'],
                             message=f'server_coro aborted, {type(ex)}, {ex}')
                # print(f'\nasyncserver, server_coro aborted, {type(ex)}, {ex}')

    async def _main(self):

        # print('\nasyncserver, _main, started')
        self._log.info(['_main'],
                    message='started')
        self._tasks.append(asyncio.create_task(self._start_server()))
        self._tasks.append(asyncio.create_task(self._schedule_recive_data_tasks()))
        self._tasks.append(asyncio.create_task(self._connections_monitor()))
        self._tasks.append(asyncio.create_task(self._start_stream()))


        # print('\nasyncserver, _main, tasks appended -> wait')
        self._log.info(['_main'],
                    message='tasks appended -> wait')
        done, pending = await asyncio.wait(self._tasks , return_when=asyncio.FIRST_EXCEPTION)

        self._capture_input.unsupress_user_input()

        for task in done:
            self._log.info(['_main'],
                        message=f'done tasks:{task}')
            # print(f'\nasyncserver, _main, done tasks:{task}')
        for task in pending:
            self._log.info(['_main'],
                        message=f'pending tasks:{task}')
            # print(f'\nasyncserver, _main, pending tasks:{task}')

        tasks = asyncio.all_tasks()
        for task in tasks:
            try:
                self._log.info(['_main'],
                            message=f'CANCELING>>> task:{task}')
                # print(f'\nCANCELING>>> task:{task}')
                task.cancel()
                self._log.info(['_main'],
                            message=f'task:{task.get_name()} <<<CANCELED')
                # print(f'\ntask:{task.get_name()} <<<CANCELED')
            except Exception as ex:
                self._log.critical(['_main'],
                                message=f'task.cancel(), {type(ex)}, {ex}')
                # print(f'\nasyncserver, _main, task.cancel(), {type(ex)}, {ex}')
        
        self._log.info(['_main'],
                    message='exited.')
        # print('\nasyncserver, _main() exited.')

    def start(self):
         asyncio.run(self._main(), debug=True)

    def close(self):
        self._capture_input.unsupress_user_input()
        try:
            self._log.info(['close'],
                        message='removing shortcuts')
            self._shortcut.remove_all_shortcuts()
        except Exception as ex:
            self._log.critical(['close'],
                            message=f'excption raised while tyring to remove shortcus, {type(ex)}, {ex}')
        else:
            self._log.info(['close'],
                        message='removing shortcuts, shortcus REMOVED')
        self._log.info(['close'],
                    message='setting _abort_tasks to True...')
        self._abort_tasks = True
        





#Now each client has an associated shortcut

#The client and its shortcut -among others- are saved in self._connected_clients_all

#When we define a shortcut, the listner will start automatically
#   and the target function will be called when the shortcut is pressed

#When the user press a pre-defined shortcut -> this will call the fcuntion "_shortcut_handle"
#   and pass the pressed shortcut

#"shortcut_handle" will check which client is associated with this shortcut and
#   starts streaming >>>

#How this is going to be done;

#Check is_streaming
#   True -> stop_stream
#           set active
#           start_stream

#   False -> set_active
#            start_stream






















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