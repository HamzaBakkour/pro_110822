import unittest
import time
import socket
from pynput.mouse import Controller as MC, Button
from pynput.keyboard import Controller as KC
from PySide6.QtCore import QThreadPool

import sys
sys.path.append('../pro_110822')
from senduserinput import SendUserInput
from reciveuserinput import ReciveUserInput
from serverworker import ServerWorker


class SenduserinputTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print("TEST STARTED")
        # try:
        #     cls.serverSocket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     cls.serverSocket.bind(('localhost',0))
        #     cls.serverSocket.listen(5)
        #     cls.serverPort = cls.serverSocket.getsockname()[1]
        #     print(f'cls.serverPort {cls.serverPort}')
        # except Exception as ex:
        #     print(f'Failed to create server socket\nTests that use server socket will fail\n{ex}')

        # try:
        #     cls.clientSocket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     cls.clientSocket.setblocking(True)
        #     cls.serverSocket.setblocking(True)
        #     cls.clientSocket.connect(('localhost', cls.serverPort))
        #     cls.serverConnection, _ = cls.serverSocket.accept()
        # except Exception as ex:
        #     print(f'Failed to create client socket\nTests that use client socket will fail\n{ex}')


    @classmethod
    def tearDownClass(cls) -> None:
        print("TEST ENDED")

    def test_start_stop_listner(self):
        testedModule = SendUserInput()
        testedModule.start_listning()
        self.assertEqual(testedModule.mouseListner.running, True, "mouseListner failed to run")
        self.assertEqual(testedModule.keyboardListner.running, True, "keyboardListner failed to run")
        testedModule.stop_listning()
        self.assertEqual(testedModule.mouseListner.running, False, "mouseListner failed to stop")
        self.assertEqual(testedModule.keyboardListner.running, False, "keyboardListner failed to stop")

    def test_hide_mouse_pointer_process(self):
        testedModule = SendUserInput()
        testedModule.start_listning()
        testedModule.supress_user_input(True)
        time.sleep(1)
        testedModule.supress_user_input(False)
        testedModule.stop_listning()
        self.assertEqual(testedModule.coverScreenProcess.returncode, None, "cover screen process error")
        self.assertEqual(testedModule.mouseListner.running, False, "mouseListner failed to stop")
        self.assertEqual(testedModule.keyboardListner.running, False, "keyboardListner failed to stop")

    def test_supress_mouse_click(self):
        mouse = MC()
        testedModule = SendUserInput()
        testedModule.start_listning()
        testedModule.supress_user_input(True)
        mouse.press(Button.left)
        time.sleep(1)
        self.assertEqual(testedModule.mouseListner._suppress, True)
        mouse.release(Button.left)  
        testedModule.supress_user_input(False)
        testedModule.stop_listning()
        self.assertEqual(testedModule.mouseListner.running, False, "mouseListner failed to stop")
        self.assertEqual(testedModule.keyboardListner.running, False, "keyboardListner failed to stop")

    def test_supress_keyboard_click(self):
        keyboard = KC()
        testedModule = SendUserInput()
        testedModule.start_listning()
        testedModule.supress_user_input(True)
        keyboard.press('A')
        time.sleep(1)
        self.assertEqual(testedModule.keyboardListner._suppress, True)
        keyboard.release('A')
        testedModule.supress_user_input(False)
        testedModule.stop_listning()
        self.assertEqual(testedModule.mouseListner.running, False, "mouseListner failed to stop")
        self.assertEqual(testedModule.keyboardListner.running, False, "keyboardListner failed to stop")

    def test_send_mouse_input_to_client(self):
        pass
        # mouse = MC()
        # serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # serverSocket.setblocking(False)
        # serverSocket.bind(('', 12345))
        # serverWorker = ServerWorker(serverSocket)
        # threabool = QThreadPool()
        # threabool.setMaxThreadCount(5)
        # threabool.start(serverWorker)
        # serverPort = serverSocket.getsockname()[1]
        # testedModule2 = ReciveUserInput('localhost', serverPort)
        # testedModule1 = SendUserInput()
        # testedModule1.send_input_to_client(testedModule2.reciveSocket)
        # mouse.move(5,5)
        # print(testedModule2.run().data)
        # serverSocket.close()
        # mouse = MC()
        # testedModule1 = SendUserInput()
        # testedModule.start_listning()
        # SenduserinputTest.clientSocket.setblocking(False)
        # SenduserinputTest.serverSocket.setblocking(False)
        # testedModule.send_input_to_client(SenduserinputTest.clientSocket)
        # mouse.move(5,5)
        # for _ in range(10):
        #     print (SenduserinputTest.clientSocket.recv(1).decode())
        #     time.sleep(1)
        









if __name__ == '__main__':
    unittest.main()
