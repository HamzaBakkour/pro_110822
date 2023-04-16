import unittest
import socket
import asyncio
import time
from random import randint
from pro_110822.prologging import Log 
from socket import SHUT_RDWR
from asyncio.exceptions import CancelledError
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


_TESTS_TIMEOUT_ = [{'test_name' : 'test_asyncclient_2.TestAsyncclient.test_connect_to_server',
                    'timeout' : 4},
                    {'test_name' : 'test_asyncclient_2.TestAsyncclient.test_send_recive_messages',
                     'timeout' : 5}]


class TestAsyncclient(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._addr = None
        self._reader = None
        self._writer = None
        self._server = None
        self._client = None
        self._tasks = []
        self._sent_messages = []
        self._recived_messages = []

        self._log = Log()

    def _get_test_timeout(self):
        test_name = unittest.TestCase.id(self)
        for timeout in _TESTS_TIMEOUT_:
            if timeout['test_name'] == test_name:
                self._log.info(['_get_test_timeout'],
                               message=f"test:{test_name}, RETURNING timeout:{timeout['timeout']}")
                return timeout['timeout']
        self._log.warning(['_get_test_timeout'],
                          message=f'test:{test_name}, NO TIMEOUT found.')
        return False

    def setUp(self):
        timeout = self._get_test_timeout()
        if timeout:
            self._log.info(['setUp'],
                           message=f'STARTING server and client tasks with timeout: {timeout}s')
            self._start_test_tasks(test_name = unittest.TestCase.id(self) ,timeout = timeout)
            return
        self._log.warning(['setUp'],
                        message=f'NO TIMEOUT test:{unittest.TestCase.id(self)}')

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
        self._sent_messages = []
        self._recived_messages = []
        self._server = None
        self._client = None

    def _start_test_tasks(self, test_name, timeout):
        try:
            asyncio.run(self._async_start_test_tasks(test_name, timeout))
        except asyncio.exceptions.TimeoutError:
            pass

    async def _async_start_test_tasks(self, test_name, timeout):
        match test_name:
            case 'test_asyncclient_2.TestAsyncclient.test_connect_to_server':
                self._tasks.append(asyncio.create_task(self._client_task()))
                self._tasks.append(asyncio.create_task(self._server_task()))

            case 'test_asyncclient_2.TestAsyncclient.test_send_recive_messages':
                self._tasks.append(asyncio.create_task(self._client_task()))
                self._tasks.append(asyncio.create_task(self._server_task()))  
                self._tasks.append(asyncio.create_task(self._recive_messages_tasks()))   
                self._tasks.append(asyncio.create_task(self._send_message_task()))
                    
        awaitables = asyncio.gather(*self._tasks)
        try:
            await asyncio.wait_for(awaitables, timeout=timeout)
        except asyncio.exceptions.TimeoutError:
            pass

    async def _client_task(self):
        print('_client_task start')
        self._client = AsyncClient()
        await self._client._main('127.0.0.1', 8888)  
        print('_client_task end')

    async def _server_task(self):
        print('_server_task start')
        async def _server_handler(reader, writer):
            addr = writer.get_extra_info('peername')
            self._log.info(['_server_handler'],
                        message=f'{addr!r} is connected.')
            print('_server_task, setting addr, writer, reader')
            self._addr = addr
            self._writer = writer
            self._reader = reader

            print('_server_task, setting addr, writer, reader. DONE')
            print(f'_server_handler, self._client:{self._client}')
            print(f'_server_handler, self._writer:{self._writer}')
            print(f'_server_handler, self._reader:{self._reader}')

        print('_server_task 1')
        await asyncio.start_server(_server_handler, '127.0.0.1', 8888)  
        print('_server_task end')

    async def _send_message_task(self):
        await asyncio.sleep(1)
        while True:
            try:
                message = f'{randint(0, 9)}'*30
                await self._client._send_data(message)
                self._sent_messages.append(message)
                await asyncio.sleep(0.1)
            except AttributeError:
                await asyncio.sleep(0.1)
                continue

    async def _recive_messages_tasks(self):
        while True:
            try:
                data = await self._reader.read(1042)
                self._recived_messages.append(data)
            except AttributeError:
                await asyncio.sleep(0.1)
                continue

    def temp_disabled_test_connect_to_server(self):
        self.assertEqual(self._addr[0],
                         '127.0.0.1')
        self.assertIsInstance(self._writer,
                              asyncio.streams.StreamWriter)
        
        self.assertIsInstance(self._reader,
                              asyncio.streams.StreamReader)

    def test_send_recive_messages(self):

        self.assertGreater(len(self._recived_messages),
                           5)

        self.assertEqual(len(self._sent_messages),
                         len(self._recived_messages))
        
        for element in zip(self._sent_messages,
                           self._recived_messages):
            self.assertEqual(element[0],
                             element[1].decode()[:-1])
            
        for message in self._recived_messages:
            self.assertEqual(len(message),
                             31)
            self.assertEqual(message.decode()[30],
                             '&')
        print('')


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




#asyncio.run(func(parameter_1, parameter_2))
#parameter_1: awaitables; gathered
#parameter_2: timeout; int

#func()
#   await_for(parameter_1, timeout = parameter_2)




        # socketThread = threading.Thread(target=self._server_socket, args=(1,))


            # self.fail('XXXXXXTIMEOUTXXXX')
        # print(f'xxx { self._addr}, {self._writer}, {self._reader}')



#asyncio.run(func(parameter_1, parameter_2))
#parameter_1: awaitables; gathered
#parameter_2: timeout; int

#func()
#   await_for(parameter_1, timeout = parameter_2)
    # def test_send_message_to_server(self):
    #     # client = AsyncClient()
    #     # socketThread = threading.Thread(target=self._server_socket, args=(1,), 
    #     #                                 kwargs={'recive_message' : True,
    #     #                                         'to_be_recived' : 5})
    #     # socketThread.start()
    #     # time.sleep(2)
    #     # timer = Timer(1)
    #     # timer.start()

    #     # time.sleep(5)

    #     pass


    # def _timer_thread(self, time_):

    # def _server_socket(self,
    #                    break_at = 1,
    #                    recive_message = False,
    #                    to_be_recived = 1,
    #                    send_message = False, 
    #                    to_be_sent = 1,
    #                    messages = []):
    #     self._server_socket_accepted_requsts = 0
    #     self._server_socket_port = None
    #     self._server_socket_recived_messages = []

    #     tempSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     tempSocket.bind(('localhost', 0))
    #     self._server_socket_port = tempSocket.getsockname()[1]
    #     conn = socket.socket()
    #     while(True):
    #         tempSocket.listen(1)
    #         conn, addr = tempSocket.accept()
    #         self._server_socket_accepted_requsts +=  1
    #         # if recive_message:
    #             # for _ in range(1, to_be_recived):

    #         if (self._server_socket_accepted_requsts == break_at):#One working ip addresses in _pre_defined_hosts_list_
    #             break
    #     self.assertEqual(self._server_socket_accepted_requsts,
    #                      break_at)
    #     conn.shutdown(SHUT_RDWR)
    #     conn.close()
