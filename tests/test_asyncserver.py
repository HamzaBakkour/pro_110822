import unittest
import asyncio
import random
from pro_110822.server.asyncserver import AsyncServer
# try:
#     from prologging import Log
# except ModuleNotFoundError:
from pro_110822.prologging import Log



_TESTS_TIMEOUT_ = [{'test_name': 'test_asyncserver.TestAsyncServer.test_accept_connection',
                    'timeout': 3},
                    {'test_name': 'test_asyncserver.TestAsyncServer.test_info_requset',
                    'timeout': 3},
                    {'test_name': 'test_asyncserver.TestAsyncServer.test_broadcast',
                    'timeout': 13},
                    {'test_name': 'test_asyncserver.TestAsyncServer.test_connections_monitor',
                    'timeout': 10},
                    {'test_name': 'test_asyncserver.TestAsyncServer.test_shortcut_handler',
                    'timeout': 7}
                    ]



class TestAsyncServer(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._client = None
        self._server = None
        self._test_client_writer = None
        self._test_client_reader = None
        self._recived_messages__by_client = []
        self._connected_test_clients = []
        self._tasks = []

        self._log = Log()

    def _get_timeout(self , test_name):
        for timeout in _TESTS_TIMEOUT_:
            if timeout['test_name'] == test_name:
                self._log.info(['_get_test_timeout'],
                               message=f"test:{test_name}, RETURNING timeout:{timeout['timeout']}")
                return timeout['timeout']
        self._log.warning(['_get_test_timeout'],
                          message=f'test:{test_name}, NO TIMEOUT found.')
        return False

    def setUp(self):
        test_name = unittest.TestCase.id(self)
        timeout = self._get_timeout(test_name)
        if timeout:
            self._log.info(['setUp'],
                           message=f'STARTING {test_name} tasks with timeout: {timeout}s')
            self._start_test_tasks(test_name = test_name ,timeout = timeout)
            return
        self._log.warning(['setUp'],
                        message=f'NO TIMEOUT test:{test_name}')

    def _start_test_tasks(self, test_name, timeout):
        try:
            asyncio.run(self._async_start_test_tasks(test_name, timeout))
        except asyncio.exceptions.TimeoutError:
            pass

    async def _async_start_test_tasks(self, test_name, timeout):
        match test_name:
            case 'test_asyncserver.TestAsyncServer.test_accept_connection':
                self._tasks.append(asyncio.create_task(self._server_task()))
                self._tasks.append(asyncio.create_task(self._client_task()))

            case 'test_asyncserver.TestAsyncServer.test_info_requset':
                self._tasks.append(asyncio.create_task(self._server_task()))
                self._tasks.append(asyncio.create_task(self._client_task()))
                self._tasks.append(asyncio.create_task(self._respond_to_info_requset()))

            case 'test_asyncserver.TestAsyncServer.test_broadcast':
                self._tasks.append(asyncio.create_task(self._server_task()))
                for client_num in range(8):
                    self._tasks.append(asyncio.create_task(self._broadcast_client(client_num)))
                self._tasks.append(asyncio.create_task(self._broadcast_task()))

            case 'test_asyncserver.TestAsyncServer.test_connections_monitor':
                self._tasks.append(asyncio.create_task(self._server_task()))
                for _ in range(5):
                    self._tasks.append(asyncio.create_task(self._connections_monitor_client()))

            case 'test_asyncserver.TestAsyncServer.test_shortcut_handler':
                self._tasks.append(asyncio.create_task(self._server_task()))
                for client_num in range(8):
                    self._tasks.append(asyncio.create_task(self._shortcut_handler_client(client_num)))

#test_connections_monitor

        awaitables = asyncio.gather(*self._tasks)
        try:
            await asyncio.wait_for(awaitables, timeout=timeout)
        except asyncio.exceptions.TimeoutError:
            pass

    def tearDown(self):
        try:
            self._server.close()
        except Exception as ex:
            self.fail(f'{type(ex)}, {ex}')

        if self._test_client_writer != None:
            try:
                self._test_client_writer.close()
            except RuntimeError:#writer is allready closed
                pass
            except Exception as ex:
                self.fail(f'{type(ex)}, {ex}')

        try:
            for task in self._tasks:
                task.cancel()
        except Exception as ex:
            self.fail(f'{type(ex)}, {ex}')

        self._client = None
        self._server = None
        self._test_client_writer = None
        self._test_client_reader = None
        self._recived_messages__by_client = []
        self._tasks = []
        self._connected_test_clients = []

    async def _client_task(self):
        await asyncio.sleep(1)
        self._test_client_reader, self._test_client_writer = await asyncio.open_connection('127.0.0.1', 8888)

    async def _server_task(self):
        self._server = AsyncServer('127.0.0.1', 8888)
        await self._server._main()

    def test_accept_connection(self):
        self.assertEqual(len(self._server.connected_clients),
                         1)
        
        self.assertEqual(self._server.connected_clients[0][0][0],
                         '127.0.0.1')

    async def _respond_to_info_requset(self):
        while(True):
            if self._test_client_writer == None:
                await asyncio.sleep(0.1)
                continue
            data = await self._test_client_reader.read(1042)
            self._recived_messages__by_client.append(data)
            if data == b'$INFO_R&':
                respond = '€INFO_R!TEST_CLIENT!SCREEN_WIDTH!SCREEN_HIGHT&'
                self._test_client_writer.write(respond.encode())
                await self._test_client_writer.drain()

    def test_info_requset(self):
        self.assertEqual(len(self._server.connected_clients),
                         1)
        self.assertEqual(self._server.connected_clients[0][0][0],
                         '127.0.0.1')
        self.assertEqual(self._server.connected_clients[0][1],
                         'TEST_CLIENT')
        self.assertEqual(self._server.connected_clients[0][2][0],
                         'SCREEN_WIDTH')
        self.assertEqual(self._server.connected_clients[0][2][1],
                         'SCREEN_HIGHT')

    async def _broadcast_client(self, client_num):
        reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
        
        data = await reader.read(1042)
        await asyncio.sleep(random.random())
        if data == b'$INFO_R&':
            respond = '€INFO_R!TEST_CLIENT!SCREEN_WIDTH!SCREEN_HIGHT&'
            writer.write(respond.encode())
            await writer.drain()

        data = b'*&'
        while data == b'*&':
            data = await reader.read(1042)
            await asyncio.sleep(random.random())
            if data != b'*&':
                data = data.decode()
                data = data.replace('*', '')
                data = data.replace('&', '')
                self._recived_messages__by_client.append(str(client_num) + data)

    async def _broadcast_task(self):
        while(len(self._server.connected_clients) < 8):
            await asyncio.sleep(0.1)
        await self._server.async_broadcast('THIS IS BROADCAST MESSAGE'.encode())

    def test_broadcast(self):
        self.assertEqual(len(self._server.connected_clients),
                         8)

        self.assertEqual(len(self._recived_messages__by_client),
                         8)

        client_num = []
        for message in self._recived_messages__by_client:
            self.assertEqual(message[1:],
                             'THIS IS BROADCAST MESSAGE')
            self.assertNotIn(message[:1],
                             client_num)
            client_num.append(message[:1])

        clients_ports = []
        for client in self._server.connected_clients:
            self.assertNotIn(client[0][1],
                             clients_ports,
                             '...')
            clients_ports.append(client[0][1])








        print('')

    async def _connections_monitor_client(self):
        await asyncio.sleep(1)
        _, writer = await asyncio.open_connection('127.0.0.1', 8888)
        self._connected_test_clients.append(writer)
        await asyncio.sleep(random.random())
        writer.close()
        await writer.wait_closed()       

    def test_connections_monitor(self):
        self.assertEqual(len(self._connected_test_clients),
                         5)

        self.assertEqual(len(self._server.connected_clients),
                         0)

        for client in self._connected_test_clients:
            self.assertTrue(client._loop._closed)

    async def _shortcut_handler_client(self, client_num):
        reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
        data = await reader.read(1042)
        await asyncio.sleep(random.random())
        if data == b'$INFO_R&':
            respond = f'€INFO_R!TEST_CLIENT{str(client_num)}!SCREEN_WIDTH!SCREEN_HIGHT&'
            writer.write(respond.encode())
            await writer.drain()

    def test_shortcut_handler(self):

        shortcuts = []
        for client in self._server._connected_clients_all:
           self.assertNotIn(client['shortcut'],
                             shortcuts)
           self.assertEqual(client['shortcut'],
                            f"<ctrl>+m+{str(client['id'])}")
           
           shortcuts.append(client['shortcut'])
        
        clients_names = []
        for client in self._server._connected_clients_all:
           self.assertNotIn(client['name'],
                             clients_names)
           clients_names.append(client['name'])

        clients_id = []
        for client in self._server._connected_clients_all:
           self.assertNotIn(client['id'],
                             clients_id)
           clients_id.append(client['id'])
        