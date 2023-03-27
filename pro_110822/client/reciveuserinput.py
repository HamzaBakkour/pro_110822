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
# from . import prologging
# from prologging import Log
from pro_110822.prologging import Log

log = Log(20)


class ReciveUserInputSignals(QObject):
    serverStoped = Signal(object, object, object)


class ReciveUserInput(QRunnable):
    def __init__(self, serverIP: str, serverPort: str, id : int)-> None:
        super(ReciveUserInput, self).__init__()
        log.debug("**STARTED**")
        self.signal = ReciveUserInputSignals()    
        self.serverIP = serverIP
        self.serverPort = int(serverPort)
        self.alive = True
        self.id = id
        self.reciveSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mouse = MC()
        self.keyboard = KC()
        self.screenRez = (0,0)
        log.debug("**EXITE**")
    
    def _get_screen_resulotion(self)-> tuple[int, int]:
        log.debug("**STARTED**")
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        log.debug(f"**EXITE** with {screensize}")
        return screensize

    def _get_pc_name(self)-> str:
        log.debug("**STARTED**")
        log.debug(f"**EXITE** with {platform.node()}")
        return platform.node()

    def _receive_n_bytes(self, n):
        log.debug("**STARTED**")
        data = ''.encode()
        while len(data) < n:
            chunk = self.conn.recv(n - len(data))
            if (chunk == ''.encode()):
                break
            data += chunk
        log.debug(f"**EXITE** with {data}")
        return data

    def _send_to_server(self):
        log.debug("**STARTED**")
        sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log.info(f"created sendSocket {sendSocket}")
        try:
            sendSocket.connect((self.serverIP, self.serverPort))
            log.info(f"connected to server {self.serverIP} at port {self.serverPort}")
        except socket.error as error:
            log.exception("Exception")
            if (error.errno == 10061):
                log.error('Socket error while trying to connect to server')
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
            log.info(f'message header + message: {header + message}')
        except Exception as ex:
            log.exception('Exception')
        sendSocket.shutdown(SHUT_RDWR)
        sendSocket.close()
        log.debug("**EXITED**")

    def _establish_connection_with_server(self):
        log.debug("**STARTED**")
        self.reciveSocket.setblocking(True)
        log.debug("[1]")
        self.reciveSocket.listen(5)
        log.debug("[2]")
        while(True):
            log.debug("[3]")
            try:
                log.debug("[4]")
                self.conn, address = self.reciveSocket.accept()
                log.debug("[5]")
                log.info(f'from receive worker accepted {self.conn} {address}')
                log.debug("[6]")
                break
            except Exception:
                log.debug("[7]")
                log.exception('Exception')
        log.debug("**EXITED**")

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
        log.debug("**EXITED**")


    @Slot()
    def run(self)-> None:
        log.debug("**STARTED**")
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
                        log.debug(f"recived {data}")
                        self._mouse_and_keyboard_controller(data)
                    else:
                        log.info('Header data value is not equal to received data length')
            except UnboundLocalError:
                pass
            except BlockingIOError:
                pass
            except IOError:
                pass
        self.conn.close()
        self.conn.shutdown(SHUT_RDWR)
        log.debug("**EXITED**")
        log.info('ReciveUserInput QRunnable terminated')
