#pro_110822/reciveuserinput.py
"""
Recive mouse and keyboard input.
"""
from PySide6.QtCore import QRunnable, Slot, QObject, Signal
from pynput.mouse import Controller as MC
from pynput.mouse import Button

from pynput.keyboard import Controller as KC
from pynput.keyboard import Key


import socket
from socket import SHUT_RDWR
import platform
import ctypes
import struct
import os
import inspect


class ReciveUserInputSignals(QObject):
    serverStoped = Signal(object, object, object)


class ReciveUserInput(QRunnable):
    def __init__(self, serverIP: str, serverPort: str, id : int)-> None:
        super(ReciveUserInput, self).__init__()
        self.signal = ReciveUserInputSignals()    
        self.serverIP = serverIP
        self.serverPort = int(serverPort)
        self.alive = True
        self.id = id
        self.reciveSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mouse = MC()
        self.keyboard = KC()
        self.screenRez = (0,0)
    
    def _get_screen_resulotion(self)-> tuple[int, int]:
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return screensize

    def _get_pc_name(self)-> str:
        return platform.node()

    def _receive_n_bytes(self, n):
        data = ''.encode()
        while len(data) < n:
            chunk = self.conn.recv(n - len(data))
            if ((chunk == ''.encode())):
                break
            data += chunk
        return data

    def _send_to_server(self):
        sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sendSocket.connect((self.serverIP, self.serverPort))
        except socket.error as error:
            if (error.errno == 10061):
                print(f'{os.path.basename(__file__)} | ',
                      f'{inspect.stack()[0][3]} | ',
                      f'[*]Socket error while trying to connect to server\nError message: {error}\nserverStoped signal emited to main thread.')
                self.signal.serverStoped.emit(self.reciveSocket, self.id, self.serverPort)
                sendSocket.close()
                sendSocket.shutdown(SHUT_RDWR)
                return
        self.screenRez = self._get_screen_resulotion()
        self.reciveSocket.bind(('',0))
        receiveSocetPort = self.reciveSocket.getsockname()[1]
        message = "C!{}!{}!{}!{}".format(self.screenRez[0], self.screenRez[1], receiveSocetPort, self._get_pc_name())
        message = message.encode()
        header = struct.pack('<L', len(message))
        try:
            sendSocket.sendall(header + message)
        except Exception as ex:
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'Exception raisde {ex}')
        sendSocket.close()
        sendSocket.shutdown(SHUT_RDWR)

    def _establish_connection_with_server(self):
        self.reciveSocket.setblocking(False)
        self.reciveSocket.listen(5)
        while(True):
            try:
                self.conn, address = self.reciveSocket.accept()
                print("from receive worker accepted {} {}".format(self.conn, address))
                break
            except BlockingIOError:
                pass

    def _mouse_and_keyboard_controller(self, message):
        match message.split('!')[0]:
            case 'M': #Mouse position
                self.mouse.position = (int((float(message.split('!')[1])*self.screenRez[0])), int((float(message.split('!')[2])*self.screenRez[1])))
            case 'P':#Mouse button
                if (message.split('!')[2] == '1'):#Mouse button pressed
                    self.mouse.press(eval(message.split('!')[1]))
                elif (message.split('!')[2] == '0'):#Mouse button released
                    self.mouse.release(eval(message.split('!')[1]))    
            case 'K': #Keyboard button          
                try:
                    if (message[4:7] == 'Key'):#Keyboard button pressed
                        self.keyboard.press(eval(message.split('!')[2]))
                    else:
                        self.keyboard.press(message.split('!')[2])
                except Exception as ex:
                    print(ex)
            case 'R': #Keyboard button released
                try:
                    self.keyboard.release(eval(message.split('!')[1]))
                except Exception as ex:
                    print(ex)
            case 'SS':
                self.signal.serverStoped.emit(self.conn, self.id, self.serverPort)  

    @Slot()
    def run(self)-> None:
        self._send_to_server()
        self._establish_connection_with_server()
        while(self.alive):
            try:
                headerData = self._receive_n_bytes(4)
                if (len(headerData) == 4):
                    dataLen = struct.unpack('<L', headerData)[0]
                    data = self._receive_n_bytes(dataLen)
                    if len(data) == dataLen:
                        data = data.decode()
                        self._mouse_and_keyboard_controller(data)
                    else:
                        print("Header data value is not equal to received data length")
            except UnboundLocalError:
                pass
            except BlockingIOError:
                pass
            except IOError:
                pass
        self.conn.close()
        self.conn.shutdown(SHUT_RDWR)
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', '---- | ' , "ReciveUserInput QRunnable terminated")
