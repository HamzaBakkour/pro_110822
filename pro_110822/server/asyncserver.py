import asyncio
from asyncio.exceptions import CancelledError
import queue
from pynput import keyboard
import time

from server.senduserinput import SendUserInput
# from server.shortcuthandle import ShortcutsHandle
from prologging import Log

import pdb

from PySide6 import QtCore
from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget
)

class TasksAborted(Exception):
    pass

class AsyncServer():
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port
        self._stream = False
        self.inbound_queue = queue.Queue(maxsize=100)
        self.clients_queue = []
        self._tasks = []
        self._abort_tasks = False
        self._writer = None
        self._reader = None
        self._capture_input = SendUserInput()

        self._shortcut_listener = None
        self._current_shortcuts = []

        

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

    @property
    def stream(self):
        return self._stream

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
        return self._stream

    def start_stream(self):

        if self._stream:
            self._log.warning(['start_stream'],
                              message=f'tryin to start stream while self._stream is {self._stream} -> RETURNING')
            return

        self._log.info(['start_stream'],
                       message='STARTING STREAM')
        try:
            self._stream = True

            self._capture_input.start_listning()

        except Exception as ex:
            self._log.error(['start_stream'],
                            message = f'{type(ex)} {ex}')

    def stop_stream(self):
        self._log.info(['stop_stream'],
                       message='STOPPING the stream')
        self.refresh_shortcuts()
        self._capture_input.stop_listning()
        self._log.info(['stop_stream'],
                       message='setting _stream to False')
        self._stream = False

    async def _start_stream(self):
        self._log.info(['_start_stream'],
                  message='STARTING')
        while(True):
            if (self._stream): 
                for _ in range(self._capture_input.events_queue.qsize()):
                    item = self._capture_input.events_queue.get()
                    if item == 'X':
                        await self._send_data(item.encode())
                        while item == 'X':
                            item = self._capture_input.events_queue.get()
                            self._log.info(['_start_stream'],
                                    message=f'item:{item} -> CALLING stop_stream')
                        self.stop_stream()
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
            shortcut_ = '<ctrl>+m+'+str(id_)
            target_function_ = 'self._shortcut_handler'
            self.define_shortcut(shortcut_, target_function_)
            self._log.info(['_client_info_respond', 'defin_ctrl_m_id_shortcut'],
                        message=f"defined shortcut: '<ctrl>+m+{str(id_)}'")
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
                        
                        raise ValueError
                    else:
                        buffer_ = buffer_ + data
                self._log.info(['_recive_data_task'],
                            message=f'client_ip:{client_ip}, client_port:{client_port} ' \
                                f'sending to buffer_extractor\nbuffer: {buffer_.decode()}')

                

                self._buffer_extractor(buffer_.decode(),  client_ip, client_port)

                failed = 0

            except (AttributeError, ValueError) as ex:
                self._log.error(['_recive_data_task'],
                              message=f'{type(ex)}, -> sleeping 0.1s + continue...')
                
                await asyncio.sleep(0.1)
                failed += 1
                if failed > 10:
                    self._log.error(['_recive_data_task'],
                                 message='reached max failed allowed RETURNING...')
                    return
                continue
            except Exception as ex:
                self._log.critical(['_recive_data_task'],
                                message=f'{type(ex)}, {ex}, RETURNING, [UNHANDELED]')
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
        for i in range(1,9):
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
                    
                    self._id_list.remove(connection['id'])

                    self._log.info(['_connections_monitor'],
                                message=f"removing shortcut: <ctrl>+m+{str(connection['id'])}")
                    
                    was_removed = False
                    try:
                        was_removed = self.remove_shortcut(connection['shortcut'])
                    except Exception as ex:
                        self._log.error(['_connections_monitor'],
                                        message=f'while trying to REMOVE SHORTCUT, {type(ex)}, {ex}'\
                                            f'\nconnection:{connection}')

                    if was_removed:
                        self._log.info(['_connections_monitor'],
                                    message=f"removing shortcut: <ctrl>+m+{str(connection['id'])}, REMOVED")
                    else:
                        self._log.info(['_connections_monitor'],
                                    message=f"removing shortcut: <ctrl>+m+{str(connection['id'])}, WAS NOT REMOVED")

                    try:
                        connection['writer'].close()
                        await connection['writer'].wait_closed()
                    except (ConnectionAbortedError, ConnectionResetError):
                        self._log.error(['_connections_monitor'],
                                     message='ConnectionAbortedError or ConnectionResetError ->' \
                                        'setting self._writer, self._reader to None if equal connection, STANDBY...')
                        try:
                            # self._capture_input.stop_listning()
                            # pdb.set_trace()
                            if (self._writer == connection['writer']) or (self._reader == connection['reader']):
                                self._writer = None
                                self._reader = None
                                if self.is_streaming():
                                    self.stop_stream()
                                    self._log.info(['_connections_monitor'],
                                                message='self._writer, self._reader is SET TO NONE + STOPPED STREAM')
                                else:
                                    self._log.info(['_connections_monitor'],
                                                message='self._writer, self._reader is NOT SET TO NONE')
                                    
                            else:
                                self._log.info(['_connections_monitor'],
                                            message='ConnectionAbortedError or ConnectionResetError, self._writer self._reader NOT SET TO None')
                        except Exception as ex:
                            self._log.critical(['_connections_monitor'],
                                               message=f'{type(ex)}, {ex}')
                            


                    except Exception as ex:
                        self._log.critical(['_connections_monitor'],
                                        message=f'{type(ex)}, {ex}')
                        # print('\nasyncserver, in _connections_monitor ', type(ex), ' ', ex)
                    connections.remove(connection)
                await asyncio.sleep(self._connections_monitor_s1_)
            await asyncio.sleep(self._connections_monitor_s2_)

    def _shortcut_handler(self, shortcut):
        if self._stream:
            self._log.info(['_shortcut_handler'],
                        message='streaming -> Return')
            return


        self._log.info(['_shortcut_handler'],
                    message=f'called with shortcut:{shortcut}')
        
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

        self._log.info(['_main'],
                    message='started')
        self._tasks.append(asyncio.create_task(self._start_server()))
        self._tasks.append(asyncio.create_task(self._schedule_recive_data_tasks()))
        self._tasks.append(asyncio.create_task(self._connections_monitor()))
        self._tasks.append(asyncio.create_task(self._start_stream()))


        self._log.info(['_main'],
                    message='tasks appended -> wait')
        done, pending = await asyncio.wait(self._tasks , return_when=asyncio.FIRST_EXCEPTION)

        self._log.info(['_main'],
                       message='CALLING unseupress_user_input')
        self._capture_input.stop_listning()

        for task in done:
            self._log.info(['_main'],
                        message=f'done tasks:{task}')
        for task in pending:
            self._log.info(['_main'],
                        message=f'pending tasks:{task}')

        tasks = asyncio.all_tasks()
        for task in tasks:
            try:
                self._log.info(['_main'],
                            message=f'CANCELING>>> task:{task}')
                task.cancel()
                self._log.info(['_main'],
                            message=f'task:{task.get_name()} <<<CANCELED')
            except Exception as ex:
                self._log.critical(['_main'],
                                message=f'task.cancel(), {type(ex)}, {ex}')
        
        self._log.info(['_main'],
                    message='exited.')

    def start(self):
         asyncio.run(self._main(), debug=True)

    def close(self):
        self._log.info(['close'],
                       message='CALLING unseupress_user_input')
        self._capture_input.stop_listning()
        try:
            self._log.info(['close'],
                        message='removing shortcuts')
            self.remove_all_shortcuts()
        except Exception as ex:
            self._log.critical(['close'],
                            message=f'excption raised while tyring to remove shortcus, {type(ex)}, {ex}')
        else:
            self._log.info(['close'],
                        message='removing shortcuts, shortcus REMOVED')
        self._log.info(['close'],
                    message='setting _abort_tasks to True...')
        self._abort_tasks = True
        


    ######## shortcut ########################################################
    def boo(self, shortcut):
        self._log.debug(['boo'],
                       message=f'called with shortcut:{shortcut}')

    def _update_listener(self):
            self._log.info(['_update_listener'],
                            message='...')
            
            if self._shortcut_listener != None:
                self._stop_listener()


            self._log.info(['_update_listener'],
                           message='UPDATING')
            

            argument = '{'
            for shortcut in self._current_shortcuts:
                argument = argument + f"'{shortcut['shortcut']}' : lambda self = self : {shortcut['target_function']}('{shortcut['shortcut']}'), "
            
            argument = argument[:-2]

            argument += '}'

            self._log.info(['_update_listener'],
                           message=f'listener argument:{argument}')

            self._shortcut_listener = keyboard.GlobalHotKeys(eval(argument))


            self._shortcut_listener.start()
    
    def define_shortcut(self, shortcut, target_function,  add_to_existing=True) -> None:
        self._log.info(['define_shortcut'],
                       message=f'called with shortcut:{shortcut}, target_function:{target_function}, add_to_existing:{add_to_existing}')


        if add_to_existing:
            self._log.info(['define_shortcut'],
                            message=f'UPDATING listener with:{self._current_shortcuts}')
            self._current_shortcuts.append({'shortcut' : shortcut, 'target_function' : target_function, 'add_to_existing' : add_to_existing})
            self._update_listener()
            return

        self._current_shortcuts = []
        self._current_shortcuts.append({'shortcut' : shortcut, 'target_function' : target_function, 'add_to_existing' : add_to_existing})
        if self._shortcut_listener != None:
            self._stop_listener()



        listener_argument = f"{{'{shortcut}' : lambda self = self : {target_function}('{shortcut}')}}"

        self._shortcut_listener =  keyboard.GlobalHotKeys(eval(listener_argument))

        self._shortcut_listener.start()
        self._log.info(['define_shortcut'],
                        message=f'Started shortcut listener with argument : {listener_argument}[-]')

    def remove_shortcut(self, to_be_removed: str)->bool:
        _was_removed_ = False
        _shortcut_exist_ = False


        for shortcut in  self._current_shortcuts:
            if shortcut['shortcut'] == to_be_removed:
                self._current_shortcuts.remove(shortcut)
                _shortcut_exist_ = True

        if not _shortcut_exist_ :
            return False

        # pdb.set_trace()

        temp = self._current_shortcuts
        self._current_shortcuts = []

        if len(temp) == 0:
            self._stop_listener()
            _was_removed_ = True
        elif  len(temp) == 1:
            self.define_shortcut(temp[0]['shortcut'], 
                                 temp[0]['target_function'],
                                 add_to_existing=False)
            _was_removed_ = True
        else :
            self.define_shortcut(temp[0]['shortcut'], 
                                 temp[0]['target_function'],
                                 add_to_existing=False)
            
            for shortcut in temp[1:]:
                self.define_shortcut(shortcut['shortcut'],
                                     shortcut['target_function'],
                                     add_to_existing=True)
            _was_removed_ = True


        return _was_removed_

    def remove_all_shortcuts(self):
        self._log.info(['remove_all_shortcuts'],
                       message='REMOVING ALL SHORTCUTS')
        self._current_shortcuts = []
        self._stop_listener()

    def _stop_listener(self):
        self._log.info(['_stop_listener'],
                       message='STOPPING >')
        if self._shortcut_listener != None:
            try:
                self._shortcut_listener.stop()
                self._shortcut_listener.join()
                self._shortcut_listener = None
                time.sleep(0.1) 
                self._log.info(['_stop_listener'],
                            message='STOPPING >> STOPPED')
            except Exception as ex:
                self._log.critical(['_stop_listener'],
                                   message=f'{type(ex)}, {ex}')
        else:
            self._log.info(['_stop_listener'],
                        message='STOPPING >> listener is ALREADY STOPED')

    def refresh_shortcuts(self):
        self._log.info(['refresh'],
                       message='REFRESHING')

        if len(self._current_shortcuts) == 0:
            self._log.warning(['refresh'],
                        message='there is no shortcuts in _current_shortcuts -> RETURNING')        
            return

        temp = self._current_shortcuts
        self.remove_all_shortcuts()

 
        if len(temp) > 1:
            self.define_shortcut(temp[0]['shortcut'],
                                 temp[0]['target_function'],
                                 add_to_existing=False)
            
            for shortcut in temp[1:]:
                self.define_shortcut(shortcut['shortcut'],
                                    shortcut['target_function'],
                                    add_to_existing=True)
            self._log.info(['refresh'],
                            message='REDEFINED shortcuts [DONE]')
            return
        

        self.define_shortcut(temp[0]['shortcut'],
                                temp[0]['target_function'],
                                add_to_existing=False)
        self._log.info(['refresh'],
                        message='REDEFINED shortcuts [DONE]')




        # self._current_shortcuts.append({'shortcut' : shortcut, 'target_function' : target_function, 'add_to_existing' : add_to_existing})


        # self._savedShortcuts = []
        # for item in args:
        #     if item not in self._savedShortcuts:
        #         self._savedShortcuts.append(item)
    ################################################################