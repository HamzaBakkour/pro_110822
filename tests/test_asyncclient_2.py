import unittest
from unittest.mock import patch
import asyncio
from random import randint
from pro_110822.prologging import Log 
import pdb
from pro_110822.client.asyncclient import AsyncClient

#######################################################
# from tests.timer import Timer
# from tests.asyncTimer import Timer
#connect to server at a given ip and port
#send and recive a message from the server
#recive an info request and send correct respond
#mouse and keyboard controller
#######################################################


_TESTS_TIMEOUT_ = [{'test_name' : 'test_asyncclient_2.TestAsyncclient.test_connect_to_test_server',
                    'timeout' : 3},
                    {'test_name' : 'test_asyncclient_2.TestAsyncclient.test_send_messages',
                     'timeout' : 4},
                    {'test_name' : 'test_asyncclient_2.TestAsyncclient.test_recive_messags',
                     'timeout' : 4},
                    {'test_name' : 'test_asyncclient_2.TestAsyncclient.test_send_and_recive_messages',
                     'timeout' : 4},
                    {'test_name' : 'test_asyncclient_2.TestAsyncclient.test_respond_to_info_requst',
                     'timeout' : 3},
                    {'test_name' : 'test_asyncclient_2.TestAsyncclient.test_mouse_and_keyboard_controller',
                     'timeout' : 3}
                     ]

#temp_disabled_

class TestAsyncclient(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._addr = None
        self._reader = None
        self._writer = None
        self._server = None
        self._client = None
        self._tasks = []
        self._sent_messages__by_server = []
        self._sent_messages__by_client = []
        self._recived_messages__by_server = []
        self._mouse_and_keyboard_events = []
        self._num_messages = 0

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
                           message=f'STARTING server and client tasks with timeout: {timeout}s')
            self._start_test_tasks(test_name = test_name ,timeout = timeout)
            return
        self._log.warning(['setUp'],
                        message=f'NO TIMEOUT test:{test_name}')

    def tearDown(self):
        try:
            self._client.close_connection()
        except Exception as ex:
            self.fail(f'{type(ex)}, {ex}')

        try:
            for task in self._tasks:
                task.cancel()
        except Exception as ex:
            self.fail(f'{type(ex)}, {ex}')

        self._tasks = []
        self._addr = None
        self._reader = None
        self._writer = None
        self._sent_messages__by_server = []
        self._sent_messages__by_client = []
        self._recived_messages__by_server = []
        self._mouse_and_keyboard_events = []
        self._num_messages = 0
        self._server = None
        self._client = None

    def _start_test_tasks(self, test_name, timeout):
        try:
            asyncio.run(self._async_start_test_tasks(test_name, timeout))
        except asyncio.exceptions.TimeoutError:
            pass

    async def _async_start_test_tasks(self, test_name, timeout):
        match test_name:
            case 'test_asyncclient_2.TestAsyncclient.test_connect_to_test_server':
                self._tasks.append(asyncio.create_task(self._client_task()))
                self._tasks.append(asyncio.create_task(self._server_task()))

            case 'test_asyncclient_2.TestAsyncclient.test_send_messages':
                self._tasks.append(asyncio.create_task(self._client_task()))
                self._tasks.append(asyncio.create_task(self._server_task()))  
                self._tasks.append(asyncio.create_task(self._recive_messages_task__by_test_server()))   
                self._tasks.append(asyncio.create_task(self._send_messages_task__by_client()))

            case 'test_asyncclient_2.TestAsyncclient.test_recive_messags':
                self._tasks.append(asyncio.create_task(self._client_task()))
                self._tasks.append(asyncio.create_task(self._server_task()))  
                self._tasks.append(asyncio.create_task(self._send_messags_task__by_test_server()))

            case 'test_asyncclient_2.TestAsyncclient.test_send_and_recive_messages':
                self._tasks.append(asyncio.create_task(self._client_task()))
                self._tasks.append(asyncio.create_task(self._server_task()))  
                self._tasks.append(asyncio.create_task(self._send_messags_task__by_test_server()))
                self._tasks.append(asyncio.create_task(self._send_messages_task__by_client()))
                self._tasks.append(asyncio.create_task(self._recive_messages_task__by_test_server()))   

            case 'test_asyncclient_2.TestAsyncclient.test_respond_to_info_requst':
                self._tasks.append(asyncio.create_task(self._mocked_client_task__info_requst()))
                self._tasks.append(asyncio.create_task(self._server_task()))  
                self._tasks.append(asyncio.create_task(self._send_info_requst_task__by_test_server()))
                self._tasks.append(asyncio.create_task(self._recive_messages_task__by_test_server()))

            case 'test_asyncclient_2.TestAsyncclient.test_mouse_and_keyboard_controller':
                self._tasks.append(asyncio.create_task(self._server_task()))
                self._tasks.append(asyncio.create_task(self._mocked_client_task__mouse_and_keyboard()))
                self._tasks.append(asyncio.create_task(self._send_mouse_and_keyboard_events__by_test_server()))  
          

        awaitables = asyncio.gather(*self._tasks)
        try:
            await asyncio.wait_for(awaitables, timeout=timeout)
        except asyncio.exceptions.TimeoutError:
            pass

    async def _client_task(self):
        self._client = AsyncClient()
        await self._client._main('127.0.0.1', 8888)  

    async def _server_task(self):
        async def _server_handler(reader, writer):
            addr = writer.get_extra_info('peername')
            self._log.info(['_server_handler'],
                        message=f'{addr!r} is connected.')
            self._addr = addr
            self._writer = writer
            self._reader = reader

        await asyncio.start_server(_server_handler, '127.0.0.1', 8888)  

    def temp_disabled_test_connect_to_test_server(self):
        self.assertEqual(self._addr[0],
                         '127.0.0.1')
        self.assertIsInstance(self._writer,
                              asyncio.streams.StreamWriter)
        
        self.assertIsInstance(self._reader,
                              asyncio.streams.StreamReader)

    def temp_disabled_test_send_messages(self):
        """send messages from client to test server """
        self.assertGreater(len(self._recived_messages__by_server),
                           15)

        self.assertEqual(len(self._sent_messages__by_client),
                         len(self._recived_messages__by_server))
        
        for element in zip(self._sent_messages__by_client,
                           self._recived_messages__by_server):
            self.assertEqual(element[0],
                             element[1].decode()[:-1])
            
        for message in self._recived_messages__by_server:
            self.assertEqual(len(message),
                             31)
            self.assertEqual(message.decode()[-1:],
                             '&')

    def temp_disabled_test_recive_messags(self):
        """send messages from test server to client"""
        self.assertEqual(len(self._sent_messages__by_server),
                               len(self._client.recived_messages))
        

        for element in zip(self._sent_messages__by_server,
                           self._client.recived_messages):
            self.assertEqual(element[0][:-1],
                             element[1])
            
        for message in self._client.recived_messages:
            self.assertEqual(len(message),
                             30)

    async def _send_messags_task__by_test_server(self):
        await asyncio.sleep(1)
        while True:
            message = f'{randint(0, 9)}'*30
            message = message + '&'
            self._writer.write(message.encode())
            self._sent_messages__by_server.append(message)
            await self._writer.drain()
            await asyncio.sleep(0.1)

    async def _send_messages_task__by_client(self):
        await asyncio.sleep(1)
        while True:
            try:
                message = f'{randint(0, 9)}'*30
                if self._num_messages % 2 == 0 :
                    await self._client._send_data(message)
                    self._sent_messages__by_client.append(message)
                    self._num_messages += 1
                else:
                    await asyncio.sleep(0.1)
            except AttributeError:
                await asyncio.sleep(0.1)
                continue

    async def _recive_messages_task__by_test_server(self):
        while True:
            try:
                data = await self._reader.read(1042)
                self._recived_messages__by_server.append(data)
                self._num_messages += 1
            except AttributeError:
                await asyncio.sleep(0.1)
                continue

    def temp_disabled_test_send_and_recive_messages(self):

        if self._num_messages % 2 != 0:
            self._send_messages_task__by_client.pop()

        self.assertGreater(len(self._sent_messages__by_client),
                           5)
        
        self.assertGreater(len(self._sent_messages__by_server),
                           5)

        self.assertEqual(len(self._sent_messages__by_client), 
                         len(self._recived_messages__by_server))
              
        self.assertEqual(len(self._sent_messages__by_server),
                         len(self._client.recived_messages))
        
        for element in zip(self._sent_messages__by_server,
                           self._client.recived_messages):
            self.assertEqual(element[0][:-1],
                             element[1])
            
            self.assertEqual(len(element[1]),
                             30)
            
        for element in zip(self._sent_messages__by_client,
                           self._recived_messages__by_server):
            self.assertEqual(element[0],
                             element[1][:-1].decode())
            
            self.assertEqual(len(element[1]),
                             31)
            
            self.assertEqual(element[1][-1:],
                             b'&')  

    @patch('pro_110822.client.asyncclient.AsyncClient._get_pc_name',
           return_value = 'THIS-IS-CLIENT-PC-NAME',
           autospec=True)
    @patch('pro_110822.client.asyncclient.AsyncClient._get_screen_resulotion',
           return_value = ('SCREEN_WIDTH', 'SCREEN_HIGHT'),
           autospec=True)
    async def _mocked_client_task__info_requst(self, pc_name, screen_res):
        self._client = AsyncClient()
        await self._client._main('127.0.0.1', 8888) 

    async def _send_info_requst_task__by_test_server(self):
        await asyncio.sleep(1)
        message = '$INFO_R'
        message = message + '&'
        self._writer.write(message.encode())
        self._sent_messages__by_server.append(message)
        await self._writer.drain()

    #info requests are snet by the server to ask the client about its name, 
    # screen width and screen hight.
    def temp_disabled_test_respond_to_info_requst(self):
        self.assertEqual(len(self._recived_messages__by_server),
                         1)
        
        self.assertEqual(len(self._sent_messages__by_server),
                         1)
        
        #info requsts messags are not added to the recived messages queu.
        self.assertEqual(len(self._client.recived_messages),
                         0)
        
        self.assertEqual(self._recived_messages__by_server[0].decode(),
                         '€INFO_R!THIS-IS-CLIENT-PC-NAME!SCREEN_WIDTH!SCREEN_HIGHT&')








    def _mocked_mouse_and_keyboard_controllers(self, x):
        print('VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV')
        # self._mouse_and_keyboard_events.append((x, y))


    async def _mocked_client_task__mouse_and_keyboard(self):
        self._client = AsyncClient()
        with patch.object(self._client, "_mouse_and_keyboard_controller",
                          side_effect = self._mocked_mouse_and_keyboard_controllers):
            await self._client._main('127.0.0.1', 8888) 

    async def _send_mouse_and_keyboard_events__by_test_server(self):
        await asyncio.sleep(1) #event = f'%!M!{x/self._screen_width}!{y/self._screen_hight}!&'
        message = '%!M!5!3!'
        message = message + '&'
        self._writer.write(message.encode())
        self._sent_messages__by_server.append(message)
        await self._writer.drain()

    def test_mouse_and_keyboard_controller(self):
        #_mocked_client_task__mouse_and_keyboard
        #_server_task
        #_send_mouse_and_keyboard_events__by_test_server
        print('NOT IMPLEMENTED YET')

if __name__ == '__main__':
    unittest.main()







    # async def _send_and_recive_messages_tasks(self):
    #     self._tasks.append(asyncio.create_task(self._send_message_task()))
    #     self._tasks.append(asyncio.create_task(self._recive_messages_tasks()))


    # async def _client_task(self):
    #     client = AsyncClient()
    #     await client._main('127.0.0.1', 8888)

    # async def _server_task(self):

    #     async def _server_handler(reader, writer):
    #         addr = writer.get_extra_info('peername')
    #         self._log.info(['_server_handler'],
    #                     message=f'{addr!r} is connected.')
    #         self._addr = addr
    #         self._writer = writer
    #         self._reader = reader


    #     await asyncio.start_server(_server_handler, '127.0.0.1', 8888)

    # async def _connect_to_server(self, timeout):
    #     tasks = []
    #     tasks.append(asyncio.create_task(self._client_task()))
    #     tasks.append(asyncio.create_task(self._server_task()))
    #     awaitables = asyncio.gather(*tasks)

    #     await asyncio.wait_for(awaitables, timeout=timeout)

    # def test_connect_to_server(self):
    #     try:
    #         asyncio.run(self._connect_to_server(timeout=3))
    #     except asyncio.exceptions.TimeoutError:
    #         pass

    #     self.assertEqual(self._addr[0],
    #                      '127.0.0.1')
    #     self.assertIsInstance(self._writer,
    #                           asyncio.streams.StreamWriter)
        
    #     self.assertIsInstance(self._reader,
    #                           asyncio.streams.StreamReader)



    # async def _send_message_task(self):
    #     print('xxx SENT 1')
    #     client = AsyncClient()
    #     print('xxx SENT 2')
    #     await client._main('127.0.0.1', 8888)
    #     print('xxx SENT 22')
    #     n = 0
    #     while n < 2:
    #         try:
    #             print('xxx SENT 3')
    #             await client._send_data('hello')
    #             print('xxx SENT 4')
    #         except Exception as ex:
    #             print(f'_sendX: {type(ex)}, {ex}')
    #             continue
    #         n += 1

    # async def _recive_message_task(self):
    #     while True:
    #         try:
    #             data = await self._reader.read(1042)
    #         except AttributeError:
    #             await asyncio.sleep(0.1)
    #             continue
    #         print('xxx Added')
    #         self._recived_messages.append(data)

    # async def _send_recive_messages(self, timeout):
    #     tasks = []
    #     tasks.append(asyncio.create_task(self._send_message_task()))
    #     tasks.append(asyncio.create_task(self._server_task()))
    #     tasks.append(asyncio.create_task(self._recive_message_task()))
    #     awaitables = asyncio.gather(*tasks)

    #     await asyncio.wait_for(awaitables, timeout=timeout)

    # def test_send_recive_messages(self):
    #     try:
    #         asyncio.run(self._send_recive_messages(timeout=50))
    #     except asyncio.exceptions.TimeoutError:
    #         pass
    #     print('')

    #     # self.assertEqual(self._addr[0],
    #     #                  '127.0.0.1')
    #     # self.assertIsInstance(self._writer,
    #     #                       asyncio.streams.StreamWriter)
        
    #     # self.assertIsInstance(self._reader,
    #     #                       asyncio.streams.StreamReader)

    












        # self._addr = None
        # self._reader = None
        # self._writer = None
        # self._sent_messages = []
        # self._recived_messages = []
        # if self._client != None:
        #     try:
        #         self._client.close_connection()
        #         time.sleep(2)
        #     except Exception as ex:
        #         self.fail(f'{type(ex)}, {ex}')
        # self._client = None


# mouse and keyboard kontroller