from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from pynput import mouse, keyboard#.mouse import Listener, Controller
import socket
import struct

import sys
import os
import traceback
import logging
import time
import re

import pdb


class SendMouseKeyboard():
    def __init__(self):
        self.activeConnection = 0

    def set_active_socket(self, active : socket.socket):
        self.activeSocket = active


    def _on_move(self, x, y):
        message = f'M!{x}!{y}'
        message = message.encode()
        self.activeConnection.send()
        header = struct.pack('<L', len(message))
        try:
            self.activeSocket.sendall(header + message)
        except Exception as e:
            print(str(e))

        # print('Pointer moved to {0}'.format(
        #     (x, y)))



    def _on_click(self, x, y, button, pressed):
        if pressed:
            message = f'P!{button}!1!{x}!{y}'
        else:
            message = f'P!{button}!0!{x}!{y}'
        message = message.encode()
        self.activeConnection.send()
        header = struct.pack('<L', len(message))
        try:
            self.activeSocket.sendall(header + message)
        except Exception as e:
            print(str(e))

        # print('{0} at {1}'.format(
        #     'Pressed' if pressed else 'Released',
        #     (x, y)))
        # # if not pressed:
        # #     # Stop listener
        # #     return False

    def _on_scroll(self, x, y, dx, dy):
        if dy < 0:
            message = f'S!d!{x}!{y}'
        else:
            message = f'S!u!{x}!{y}'
        message = message.encode()
        self.activeConnection.send()
        header = struct.pack('<L', len(message))
        try:
            self.activeSocket.sendall(header + message)
        except Exception as e:
            print(str(e))

        # print('Scrolled {0} at {1}'.format(
        #     'down' if dy < 0 else 'up',
        #     (x, y)))

    def _on_press(self, key):
        try:
            message = f'K!a!{key.char}'
        except AttributeError:
            message = f'K!s!{key}'
        message = message.encode()
        self.activeConnection.send()
        header = struct.pack('<L', len(message))
        try:
            self.activeSocket.sendall(header + message)
        except Exception as e:
            print(str(e))

        # try:
        #     print('alphanumeric key {0} pressed'.format(
        #         key.char))
        # except AttributeError:
        #     print('special key {0} pressed'.format(
        #         key))

    def _on_release(self, key):
        message = f'R!{key}'
        message = message.encode()
        self.activeConnection.send()
        header = struct.pack('<L', len(message))
        try:
            self.activeSocket.sendall(header + message)
        except Exception as e:
            print(str(e))

        # print('{0} released'.format(
        #     key))
        # # if key == keyboard.Key.esc:
        # #     # Stop listener
        # #     return False


    def start_listning(self):
        self.mouseListner = mouse.Listener(on_move=self._on_move, on_click=self._on_click, on_scroll=self._on_scroll)
        self.keyboardListner = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        self.mouseListner.start()
        self.keyboardListner.start()

    def set_sending_socket(self, active)-> None:
        self.activeConnection = active


# class SendMouseMovementWorkerSignals(QObject):
#     updateSignal = Signal(object)

# class SendMouseMovementWorker(QRunnable):
#     def __init__(self, clientIP: str, socketPort : str)-> None:
#         super(SendMouseMovementWorker, self).__init__()
#         print("SendMouseMovementWorker started")
#         self.clientIP = clientIP
#         self.socketPort = int(socketPort)
#         print("clientIP", self.clientIP)
#         print("socketPort", self.socketPort)
        

#     # def on_move(self, x, y):
#     #     print("sending ", x, " ",y)
#     #     self.serverSocket.send('aa{}bb{}cc'.format(x, y).encode())

#     # def on_click(self, x, y, button, pressed):
#     #     print('{} {}'.format(button, 'Pressed' if pressed else 'Released'))

#     # def on_scroll(self, x, y, dx, dy):
#     #     print('({}, {})'.format(dx, dy))

    

#     @Slot()
#     def run(self)-> int:
#         serverSocket = socket.socket()
#         host = socket.gethostname()
#         serverSocket.bind(('', self.socketPort))
#         serverSocket.listen()
#         connS, addressS = serverSocket.accept()
#         print("Connection from: " + str(addressS) + "accepted")
        
#         mouse = Controller()
#         while(True):
#             print('{0}'.format(mouse.position))
#             # pdb.set_trace()
#             connS.send('aa{}bb{}cc'.format(str(mouse.position[0]), str(mouse.position[1])).encode())