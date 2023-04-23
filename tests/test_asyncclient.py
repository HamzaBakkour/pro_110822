import unittest
from unittest.mock import patch
import asyncio
from random import randint
from prologging import Log 
import pdb
try:
    from pro_110822.client.asyncclient import AsyncClient
except ModuleNotFoundError:
    from client.asyncclient import AsyncClient

_TESTS_TIMEOUT_ = [{'test_name' : 'test_connect_to_test_server',
                    'timeout' : 3},
                    {'test_name' : 'test_send_messages',
                     'timeout' : 4},
                    {'test_name' : 'test_recive_messags',
                     'timeout' : 4},
                    {'test_name' : 'test_send_and_recive_messages',
                     'timeout' : 4},
                    {'test_name' : 'test_respond_to_info_requst',
                     'timeout' : 3},
                    {'test_name' : 'test_mouse_and_keyboard_controller',
                     'timeout' : 5}
                     ]

class TestAsyncclient(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._addr = None
        self._test_server_reader = None
        self._test_server_writer = None
        self._test_server = None
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
        test_name = test_name.split('.')[-1]
        timeout = self._get_timeout(test_name)
        if timeout:
            self._log.info(['setUp'],
                           message=f'STARTING {test_name} tasks with timeout: {timeout}s')
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
        self._test_server_reader = None
        self._test_server_writer = None
        self._sent_messages__by_server = []
        self._sent_messages__by_client = []
        self._recived_messages__by_server = []
        self._mouse_and_keyboard_events = []
        self._num_messages = 0
        self._test_server = None
        self._client = None

    def _start_test_tasks(self, test_name, timeout):
        try:
            asyncio.run(self._async_start_test_tasks(test_name, timeout))
        except asyncio.exceptions.TimeoutError:
            pass

    async def _async_start_test_tasks(self, test_name, timeout):
        match test_name:
            case 'test_connect_to_test_server':
                self._tasks.append(asyncio.create_task(self._client_task()))
                self._tasks.append(asyncio.create_task(self._server_task()))

            case 'test_send_messages':
                self._tasks.append(asyncio.create_task(self._client_task()))
                self._tasks.append(asyncio.create_task(self._server_task()))  
                self._tasks.append(asyncio.create_task(self._recive_messages_task__by_test_server()))   
                self._tasks.append(asyncio.create_task(self._send_messages_task__by_client()))

            case 'test_recive_messags':
                self._tasks.append(asyncio.create_task(self._client_task()))
                self._tasks.append(asyncio.create_task(self._server_task()))  
                self._tasks.append(asyncio.create_task(self._send_messags_task__by_test_server()))

            case 'test_send_and_recive_messages':
                self._tasks.append(asyncio.create_task(self._client_task()))
                self._tasks.append(asyncio.create_task(self._server_task()))  
                self._tasks.append(asyncio.create_task(self._send_messags_task__by_test_server()))
                self._tasks.append(asyncio.create_task(self._send_messages_task__by_client()))
                self._tasks.append(asyncio.create_task(self._recive_messages_task__by_test_server()))   

            case 'test_respond_to_info_requst':
                self._tasks.append(asyncio.create_task(self._mocked_client_task__info_requst()))
                self._tasks.append(asyncio.create_task(self._server_task()))  
                self._tasks.append(asyncio.create_task(self._send_info_requst_task__by_test_server()))
                self._tasks.append(asyncio.create_task(self._recive_messages_task__by_test_server()))

            case 'test_mouse_and_keyboard_controller':
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
            self._test_server_writer = writer
            self._test_server_reader = reader
        await asyncio.start_server(_server_handler, '127.0.0.1', 8888)  

    async def _send_messags_task__by_test_server(self):
        await asyncio.sleep(1)
        while True:
            message = f'{randint(0, 9)}'*30
            message = message + '&'
            self._test_server_writer.write(message.encode())
            self._sent_messages__by_server.append(message)
            await self._test_server_writer.drain()
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
                data = await self._test_server_reader.read(1042)
                self._recived_messages__by_server.append(data)
                self._num_messages += 1
            except AttributeError:
                await asyncio.sleep(0.1)
                continue

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
        self._test_server_writer.write(message.encode())
        self._sent_messages__by_server.append(message)
        await self._test_server_writer.drain()

    def _mouse_position_set__side_effect(self, pos):
        self._mouse_and_keyboard_events.append({'event' : 'position', 'value' : pos})

    def _mouse_press__side_effect(self, arg):
        self._mouse_and_keyboard_events.append({'event' : 'mouse_press', 'value' : arg.name})

    def _mouse_release__side_effect(self, arg):
        self._mouse_and_keyboard_events.append({'event' : 'mouse_release', 'value' : arg.name})

    def _keyboard_press__side_effect(self, arg):
        self._mouse_and_keyboard_events.append({'event' : 'keyboard_press', 'value' : arg})

    def _keyboard_release__side_effect(self, arg):
        self._mouse_and_keyboard_events.append({'event' : 'keyboard_release', 'value' : arg.name})

    @patch('pro_110822.client.asyncclient.AsyncClient._get_screen_resulotion',
           return_value = (1, 1),
           autospec=True)
    async def _mocked_client_task__mouse_and_keyboard(self, screen_res):
        self._client = AsyncClient()

        with patch.object(self._client._mouse, "_position_set",
                          side_effect = self._mouse_position_set__side_effect):

            with patch.object(self._client._mouse, "press",
                            side_effect = self._mouse_press__side_effect):
                
                with patch.object(self._client._mouse, "release",
                                side_effect = self._mouse_release__side_effect):
                    
                    with patch.object(self._client._keyboard, "press",
                                    side_effect = self._keyboard_press__side_effect):
                        
                        with patch.object(self._client._keyboard, "release",
                                            side_effect = self._keyboard_release__side_effect):

                            await self._client._main('127.0.0.1', 8888) 

    async def _send_mouse_and_keyboard_events__by_test_server(self):
        await asyncio.sleep(1)
        events = ['%!M!5!3!',
                  '%!P!Button.left!1!',
                  '%!P!Button.left!0!',
                  '%!P!Button.right!1!',
                  '%!P!Button.right!0!',
                  '%!K!a!key_a!',
                  '%!K!s!key_s!',
                  '%!R!Key.alt_l!',
                  '%!R!Key.alt_r!']
        
        for event in events:
            event = event + '&'
            self._test_server_writer.write(event.encode())
            self._sent_messages__by_server.append(event)
            await self._test_server_writer.drain()

    def test_connect_to_test_server(self):
        self.assertEqual(self._addr[0],
                         '127.0.0.1')
        self.assertIsInstance(self._test_server_writer,
                              asyncio.streams.StreamWriter)
        
        self.assertIsInstance(self._test_server_reader,
                              asyncio.streams.StreamReader)

    def test_send_messages(self):
        """send messages from client to test server """
        
        if self._num_messages % 2 != 0:
            self._sent_messages__by_client.pop()    
        
        self.assertGreater(len(self._recived_messages__by_server),
                           15)

        self.assertEqual(len(self._sent_messages__by_client),
                         len(self._recived_messages__by_server),
                         f'num messags: {self._num_messages}')
        
        for element in zip(self._sent_messages__by_client,
                           self._recived_messages__by_server):
            self.assertEqual(element[0],
                             element[1].decode()[:-1])
            
        for message in self._recived_messages__by_server:
            self.assertEqual(len(message),
                             31)
            self.assertEqual(message.decode()[-1:],
                             '&')

    def test_recive_messags(self):
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

    def test_send_and_recive_messages(self):

        if self._num_messages % 2 != 0:
            self._sent_messages__by_client.pop()

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

    #info requests are snet by the server to ask the client about its name, 
    # screen width and screen hight.
    def test_respond_to_info_requst(self):
        self.assertEqual(len(self._recived_messages__by_server),
                         1)
        
        self.assertEqual(len(self._sent_messages__by_server),
                         1)
        
        #info requsts messags are not added to the client's recived messages queu.
        self.assertEqual(len(self._client.recived_messages),
                         0)
        
        self.assertEqual(self._recived_messages__by_server[0].decode(),
                         '€INFO_R!THIS-IS-CLIENT-PC-NAME!SCREEN_WIDTH!SCREEN_HIGHT&')

    def test_mouse_and_keyboard_controller(self):
        self.assertEqual(len(self._sent_messages__by_server),
                         len(self._mouse_and_keyboard_events))
        
        self.assertEqual(self._mouse_and_keyboard_events[0]['event'],
                         'position')
        
        self.assertEqual(self._mouse_and_keyboard_events[0]['value'],
                         (5, 3))

        self.assertEqual(self._mouse_and_keyboard_events[1]['event'],
                         'mouse_press')
        
        self.assertEqual(self._mouse_and_keyboard_events[1]['value'],
                         'left')

        self.assertEqual(self._mouse_and_keyboard_events[2]['event'],
                         'mouse_release')
        
        self.assertEqual(self._mouse_and_keyboard_events[2]['value'],
                         'left')

        self.assertEqual(self._mouse_and_keyboard_events[3]['event'],
                         'mouse_press')
        
        self.assertEqual(self._mouse_and_keyboard_events[3]['value'],
                         'right')

        self.assertEqual(self._mouse_and_keyboard_events[4]['event'],
                         'mouse_release')
        
        self.assertEqual(self._mouse_and_keyboard_events[4]['value'],
                         'right')

        self.assertEqual(self._mouse_and_keyboard_events[5]['event'],
                         'keyboard_press')
        
        self.assertEqual(self._mouse_and_keyboard_events[5]['value'],
                         'key_a')
        
        self.assertEqual(self._mouse_and_keyboard_events[6]['event'],
                         'keyboard_press')
        
        self.assertEqual(self._mouse_and_keyboard_events[6]['value'],
                         'key_s')

        self.assertEqual(self._mouse_and_keyboard_events[7]['event'],
                         'keyboard_release')
        
        self.assertEqual(self._mouse_and_keyboard_events[7]['value'],
                         'alt_l')
        
        self.assertEqual(self._mouse_and_keyboard_events[8]['event'],
                         'keyboard_release')
        
        self.assertEqual(self._mouse_and_keyboard_events[8]['value'],
                         'alt_r')




if __name__ == '__main__':
    unittest.main()
