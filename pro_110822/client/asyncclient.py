import asyncio
from asyncio.exceptions import CancelledError
import queue
import platform
import pdb
from ctypes import windll
from pynput.mouse import Controller as MC
from pynput.mouse import Button

from pynput.keyboard import Controller as KC
from pynput.keyboard import Key

import sys

from pro_110822.prologging import Log

class BadConnection(Exception):
    pass

class ServerIsNotConnected(Exception):
    pass

class IntendedAbortGroupTask(Exception):
    pass

class AsyncClient():
    def __init__(self) -> None:
        self._reader = None
        self._writer = None
        self._connected = False
        self._log = Log()
        self._abort_tasks = False
        self._tasks = []
        self._raise_exeption_ = False
        self._inbound_queue = queue.Queue()
        self._outbound_queue = queue.SimpleQueue()
        self._mouse = MC()
        self._keyboard = KC()
        self._x = self._get_screen_resulotion()[0]
        self._y = self._get_screen_resulotion()[1]
        self._recive_message_s1 = 0.1
    
    @property
    def _raise_exeption(self):
        return self._raise_exeption_
    
    @_raise_exeption.setter
    def _raise_exeption(self, value):
        if type(value) != bool:
            print(f'\nasyncclient, _raise_exption, value:{value} must be of type bool')
            return
        if not self._raise_exeption_:
            self._raise_exeption_ = True
            try:
                print(f'\nasyncclient, @_raise_exeption.setter, called by {sys._getframe(1).f_code.co_name}'\
                      f"\nwith value {value}, _raise_exeption_ is now {self._raise_exeption_ }")
            except Exception:
                print('\nasyncclient, @_raise_exeption.setter, _raise_exeption_ is set to True')
        else:
            try:
                print(f'\nasyncclient, @_raise_exeption.setter, called by {sys._getframe(1).f_code.co_name}'\
                      f"\nwith value {value}, NO CHANGES MADE, _raise_exeption_ is {self._raise_exeption_}")
            except Exception:
                print(f'\nasyncclient, @_raise_exeption.setter, called with value {value}  NO CHANGES MADE [OK]')

    @property
    def is_connected(self):
        return self._connected

    def _inbound_queue_put(self, data):
        if (data != '*'):
            self._inbound_queue.put(data)
            print(f"{data} added to self._inbound_queue")

    @staticmethod
    def _pack_data(data_):
        return f'{data_}&'.encode()

    async def _connect(self, serverIP, serverPort):
        try:
            print(f"\nasyncclient, _connect, trying to connect to server {serverIP}:{serverPort}")
            self._reader, self._writer = await asyncio.open_connection(serverIP, serverPort)
        except ConnectionRefusedError:
            print(f'\nayncclient, _connect, ConnectionRefusedError {ConnectionRefusedError} -> RAISING')
            self._raise_exeption = True
            raise ConnectionRefusedError

        except Exception as ex:
            print(f'asyncclient, _connect, CANNOT CONNECT to server {type(ex)}, {ex}')
        else:
            print("\nasyncclient, _connect, connected")
            self._connected = True

    async def _can_start_recive_message_task(self, sleep_ = 0.3, allowed_failures = 20 ):
        failed = 0
        while (True):
            if not self._connected:
                print('asyncclient, in _can_start_recive_message_task, client is not connected to the server yet,'\
                      f'\ncannot start reciving message task, cheking again in {sleep_} seconds...')
                await asyncio.sleep(sleep_)
                failed += 1
                if failed > allowed_failures:
                    print(f"\nasyncclient, _can_start_recive_message_task, waited for {failed*sleep_}s"\
                          "\nasyncclient, _can_start_recive_message_task, client still not connected -> RASING EXEPTION, EXITING...")
                    raise ServerIsNotConnected
            else:
                print('\nasyncclient, _can_start_recive_message_task, cliens is now connected, STARTING recive message task')
                break

    async def _recive_message(self):

        await self._can_start_recive_message_task()

        failed = 0
        while(True):
            try:
                buffer_ = b''
                while(buffer_[-1:] != b'&'):
                    data = await self._reader.read(1024)
                    # print(f'asyncclient, recive_message, data:{data}')
                    if not data:
                        print('\nasyncclient, _recive_message, not data -> break')
                        await asyncio.sleep(0.1)
                        raise ValueError
                    else:
                        buffer_ = buffer_ + data
                await self._buffer_extractor(buffer_.decode())
                
                failed = 0

            except (AttributeError, ValueError) as ex:
                print(f'\nasyncclient, in _recive_message, {type(ex)}, {ex},  -> sleeping 0.1s + continue [OK]')
                await asyncio.sleep(0.1)
                failed += 1
                if failed > 10:
                    print('\nasyncclient, in _recive_message, reached max failed allowed RAISING EXEPTION')
                    self._raise_exeption = True
                    raise BadConnection('Server closed the connection')
                continue
            except Exception as ex:
                print(f'\nasyncclient, in _recive_message, {type(ex)}, {ex}, RAISING EXEPTION -> TERMINATING...')
                raise ex

    async def _buffer_extractor(self, buffer_):
        extracted_data = buffer_.split('&')
        for data in extracted_data:
            # print(f'\nasyncclient, _buffer_extractor, data:{data}')
            if data.startswith('%'):
                self._mouse_and_keyboard_controller(data)
            elif data.startswith('$'):   
                await self._handel_server_messages(data)
            elif not data.startswith('*') and not data == '':
                self._inbound_queue.put(data)

    def _mouse_and_keyboard_controller(self, data):
        try:
            event = data.split('!')[1]
            # print(f'>>>>>>>>>> {event}')
            match event:
                case 'M': #Mouse position
                    # print('>>>>>>>>>> IN')
                    self._mouse.position = (int((float(data.split('!')[2])* self._x)), 
                                            int((float(data.split('!')[3])* self._y)))
                case 'P': #Mouse button
                    if (data.split('!')[3] == '1'):#Mouse button pressed
                            self._mouse.press(eval(data.split('!')[2]))
                    elif (data.split('!')[3] == '0'):#Mouse button released
                            self._mouse.release(eval(data.split('!')[2]))
                case 'K': #Keyboard button
                    try:
                        if (data[6:9] == 'Key'):#Keyboard button pressed
                            self._keyboard.press(eval(data.split('!')[3]))
                        else:
                            self._keyboard.press(data.split('!')[3])
                    except Exception as ex:
                        print(f'asyncclient, control_test, case K {type(ex)}, {ex}')
                case 'R': #Keyboard button released
                    try:
                        self._keyboard.release(eval(data.split('!')[2]))
                    except Exception as ex:
                        print(f'asyncclient, control_test, case R {type(ex)}, {ex}')



        except Exception as ex:
            print(f'asyncclient, control_test, {type(ex)}, {ex}')


        #     if (data.split('!')[0] == 'M'):#Mouse position
        #             self._mouse.position = (int((float(data.split('!')[1])*self._get_screen_resulotion()[0])), 
        #                                     int((float(data.split('!')[2])*self._get_screen_resulotion()[1])))
        #     elif (data.split('!')[0] == 'P'):#Mouse button
        #         if (data.split('!')[2] == '1'):#Mouse button pressed
        #                 self._mouse.press(eval(self.data.split('!')[1]))
        #         elif (data.split('!')[2] == '0'):#Mouse button released
        #                 self._mouse.release(eval(self.data.split('!')[1]))
        #     elif (data.split('!')[0] == 'K'):#Keyboard button
        #         try:
        #             if (data[4:7] == 'Key'):#Keyboard button pressed
        #                 self._keyboard.press(eval(data.split('!')[2]))
        #             else:
        #                 self._keyboard.press(data.split('!')[2])
        #         except Exception as ex:
        #             print(ex)
        #     elif (data.split('!')[0] == 'R'):#Keyboard button released
        #         try:
        #             self._keyboard.release(eval(data.split('!')[1]))
        #         except Exception as ex:
        #             print(ex)
        #     elif(data == 'SS'):
        #         print('stopppppppp')
        # except Exception as ex:
        #     print(f'asyncclient, control_test, {type(ex)}, {ex}')

    async def _group_tasks_terminator(self, sleep_ = 0.5):
        while(True):
            if self._abort_tasks:
                print("\nasyncclient, _group_tasks_terminator, raising IntendedAbortGroupTask...")
                raise IntendedAbortGroupTask
            await asyncio.sleep(sleep_)

    async def _handel_server_messages(self, message):
        print(f'\nasyncclient, _handel_server_messages, recived: {message}')
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
                print(type(ex), ex, 'Unhandeledxxx')

    @property
    def recived_messages(self):
        return  list(self._inbound_queue.queue)

    async def _main(self, serverIP, serverPort):

        self._tasks.append(asyncio.create_task(self._connect(serverIP, serverPort)))
        self._tasks.append(asyncio.create_task(self._recive_message()))
        self._tasks.append(asyncio.create_task(self._group_tasks_terminator()))


        done, pending = await asyncio.wait(self._tasks , return_when=asyncio.FIRST_EXCEPTION)

        print('')
        for task in done:
            print(f'asyncserver, _main, done tasks:{task}')
        print('')
        for task in pending:
            print(f'asyncserver, _main, pending tasks:{task}')

        await self._close_connection()

        tasks = asyncio.all_tasks()

        for task in tasks:
            try:
                print(f'\nCANCELING>>> task:{task}')
                task.cancel()
                print(f'\ntask:{task.get_name()} <<<CANCELED')
            except Exception as ex:
                print(f'\nasyncclient, _main, task.cancel(), {type(ex)}, {ex}')

    async def _close_connection(self):
        try:
            self._writer.close()
            await self._writer.wait_closed()
        except (ConnectionAbortedError, ConnectionResetError) as ex:
            print(f'\nasyncclient, _close_connection, {type(ex)}, {ex} [OK]')
        except Exception as ex:
            print('\nasyncclient, _close_connection ', type(ex), ' ', ex)
            return
        print('\nasyncclient, _close_connection connection CLOSED.')

    def close_connection(self):
        self._abort_tasks = True
 
    def connect(self, serverIP, serverPort):
        try:
            asyncio.run(self._main(serverIP, serverPort))
        except CancelledError:
            if self._raise_exeption :
                self._log.info(['connect'],
                                  message = 'tasks group canceled, _raise_exeption is TRUE -> RAISING EXCEPTION + EXITING')
                raise CancelledError
            else:
                self._log.info(['connect'],
                                  message = 'tasks group canceled, _raise_exeption is FALSE -> EXITING')
        except Exception as ex:
            if self._raise_exeption :
                self._log.error(['connect'],
                                message=f'tasks group canceled, {type(ex)}, {ex}, _raise_exeption is TRUE -> RAISING EXCEPTION + EXITING')
                raise ex
            else:
                self._log.error(['connect'],
                                message=f'tasks group canceled, {type(ex)}, {ex}, _raise_exeption is FALSE -> EXITING')



        # except ConnectionRefusedError:
        #     print(f'\nasyncclient, connect, {ConnectionRefusedError}, RAISING + EXITING')
        #     raise ConnectionRefusedError
        # except CancelledError:
        #     print(f'\nasyncclient, connect, {CancelledError}, NOT RAISING + EXITING')
            





        # try:
        #     self._writer.close()
        #     asyncio.run(self._wait_on_connection_close())
        # except Exception as ex:
        #     print(type(ex))

       #     if (data.split('!')[0] == 'M'):#Mouse position
        #             self._mouse.position = (int((float(data.split('!')[1])*self._get_screen_resulotion()[0])), 
        #                                     int((float(data.split('!')[2])*self._get_screen_resulotion()[1])))
        #     elif (data.split('!')[0] == 'P'):#Mouse button
        #         if (data.split('!')[2] == '1'):#Mouse button pressed
        #                 self._mouse.press(eval(self.data.split('!')[1]))
        #         elif (data.split('!')[2] == '0'):#Mouse button released
        #                 self._mouse.release(eval(self.data.split('!')[1]))
        #     elif (data.split('!')[0] == 'K'):#Keyboard button
        #         try:
        #             if (data[4:7] == 'Key'):#Keyboard button pressed
        #                 self._keyboard.press(eval(data.split('!')[2]))
        #             else:
        #                 self._keyboard.press(data.split('!')[2])
        #         except Exception as ex:
        #             print(ex)
        #     elif (data.split('!')[0] == 'R'):#Keyboard button released
        #         try:
        #             self._keyboard.release(eval(data.split('!')[1]))
        #         except Exception as ex:
        #             print(ex)
        #     elif(data == 'SS'):
        #         print('stopppppppp')
        # except Exception as ex:
        #     print(f'asyncclient, control_test, {type(ex)}, {ex}')



                # self.signal.serverStoped.emit(self.conn, self.id, self.serverPort)
        # except UnboundLocalError:
        #     pass
        # except BlockingIOError:
        #     pass
        # except IOError:
        #     pass