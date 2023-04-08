import asyncio
from asyncio.exceptions import CancelledError
import queue
import platform
import pdb
from ctypes import windll


class TooManyAttributeErrorValueError(Exception):
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
        self._abort_tasks = False
        self._tasks = []
        self._inbound_queue = queue.Queue()
        self._outbound_queue = queue.SimpleQueue()
        self._recive_message_s1 = 0.1
    
    def is_connected(self):
        return self._connected

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
                head_length = await self._reader.read(7)
                head_length = head_length.decode()
                head_length = head_length.replace('+', '')
                head_length = int(head_length)
                data = await self._reader.read(head_length)
                data = data.decode()

                if data.startswith('$'):
                    await self._handel_server_messages(data)
                else:
                    self._inbound_queue_put(data)

                failed = 0

            except (AttributeError, ValueError) as ex:
                print(f'\nasyncclient, in _recive_message, {type(ex)}, {ex},  -> sleeping 0.1s + continue [OK]')
                await asyncio.sleep(0.1)
                failed += 1
                if failed > 50:
                    print('\nasyncclient, in _recive_message, reached max failed allowed RAISING EXEPTION')
                    raise TooManyAttributeErrorValueError
                continue
            except Exception as ex:
                print(f'\nasyncclient, in _recive_message, {type(ex)}, {ex}, RAISING EXEPTION -> TERMINATING...')
                raise ex


            await asyncio.sleep(self._recive_message_s1)

    async def _group_tasks_terminator(self, sleep_ = 0.5):
        while(True):
            if self._abort_tasks:
                print("\nasyncclient, _group_tasks_terminator, raising IntendedAbortGroupTask...")
                raise IntendedAbortGroupTask
            await asyncio.sleep(sleep_)

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

        self._tasks.append(asyncio.create_task(self._connect(serverIP, serverPort)))
        self._tasks.append(asyncio.create_task(self._recive_message()))
        self._tasks.append(asyncio.create_task(self._group_tasks_terminator()))


        done, pending = await asyncio.wait(self._tasks , return_when=asyncio.FIRST_EXCEPTION)

        for task in done:
            print(f'\nasyncserver, _main, done tasks:{task}')
        for task in pending:
            print(f'\nasyncserver, _main, pending tasks:{task}')

        await self._close_connection()

        tasks = asyncio.all_tasks()

        for task in tasks:
            try:
                print(f'\nCANCELING>>> task:{task}')
                task.cancel()
                self._tasks.remove(task)
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
            print(f'\asyncclient, connect, {CancelledError}, EXITING...')

        
            





        # try:
        #     self._writer.close()
        #     asyncio.run(self._wait_on_connection_close())
        # except Exception as ex:
        #     print(type(ex))

