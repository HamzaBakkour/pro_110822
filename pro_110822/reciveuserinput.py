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
import platform
import ctypes
import struct
import os
import inspect


class ReciveUserInputSignals(QObject):
    serverStoped = Signal(object, object, object)


# self.signal.serverStoped.emit(self.conn, self.id, self.serverPort)
class ReciveUserInput(QRunnable):
    def __init__(self, serverIP: str, serverPort: str, id : int)-> None:
        super(ReciveUserInput, self).__init__()
        self.signal = ReciveUserInputSignals()    
        self.serverIP = serverIP
        self.serverPort = int(serverPort)
        self.alive = True
        self.id = id
        self.sendSocket = None
        self.reciveSocket = None
        self.data = None
        
       

    def get_screen_resulotion(self)-> tuple[int, int]:
        """
        Get the screen width and hight.

        Args:
            None

        Returns:
            tuple[secreen width, screen hight]
        """
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return screensize

    def get_pc_name(self)-> str:
        """
        Get the PC name.

        Args:
            None

        Returns:
            None
        """
        return platform.node()

    def _receive_n_bytes(self, n):
        """
        Receiving exactly n bytes from socket connection (assuming it's open and connected).
        """
        data = ''.encode()
        while len(data) < n:
            chunk = self.conn.recv(n - len(data))
            if ((chunk == ''.encode())):
                break
            data += chunk
        return data

    @Slot()
    def run(self)-> None:
        """
        The QRunnable run method. This method will be called when the QRunnable is
        started.

        Args:
            None

        Returns:
            None
        """
        #sendSocket is used to send client info to the server.
        self.sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #reciveSocket is used to recive mouse and keyboard input.
        self.reciveSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.reciveSocket.bind(('',0))
        self.reciveSocket.setblocking(0)
        try:
            self.sendSocket.connect((self.serverIP, self.serverPort))
        except socket.error as error:
            if (error.errno == 10061):
                print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'[*]Socket error while trying to connect to server\nError message: {error}\nserverStoped signal emited to main thread.')
                self.signal.serverStoped.emit(self.reciveSocket, self.id, self.serverPort)
                self.sendSocket.close()
                return
        screenRez = self.get_screen_resulotion()
        receiveSocetPort = self.reciveSocket.getsockname()[1]
        message = "C!{}!{}!{}!{}".format(screenRez[0], screenRez[1], receiveSocetPort, self.get_pc_name())
        message = message.encode()
        header = struct.pack('<L', len(message))
        try:
            self.sendSocket.sendall(header + message)
        except Exception as ex:
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'Exception raisde {ex}')
        self.reciveSocket.listen(5)
        while(True):
            try:
                self.conn, address = self.reciveSocket.accept()
                print("from receive worker accepted {} {}".format(self.conn, address))
                break
            except BlockingIOError:
                pass

        mouse = MC()
        keyboard = KC()

        while(self.alive):
            try:
                headerData = self._receive_n_bytes(4)
                if (len(headerData) == 4):
                    dataLen = struct.unpack('<L', headerData)[0]
                    self.data = self._receive_n_bytes(dataLen)
                    if len(self.data) == dataLen:
                        self.data = self.data.decode()
                        if (self.data.split('!')[0] == 'M'):#Mouse position
                            mouse.position = (int((float(self.data.split('!')[1])*screenRez[0])), int((float(self.data.split('!')[2])*screenRez[1])))
                        elif (self.data.split('!')[0] == 'P'):#Mouse button
                            if (self.data.split('!')[2] == '1'):#Mouse button pressed
                                mouse.press(eval(self.data.split('!')[1]))
                            elif (self.data.split('!')[2] == '0'):#Mouse button released
                                mouse.release(eval(self.data.split('!')[1]))
                        elif (self.data.split('!')[0] == 'K'):#Keyboard button
                            try:
                                if (self.data[4:7] == 'Key'):#Keyboard button pressed
                                    keyboard.press(eval(self.data.split('!')[2]))
                                else:
                                    keyboard.press(self.data.split('!')[2])
                            except Exception as ex:
                                print(ex)
                        elif (self.data.split('!')[0] == 'R'):#Keyboard button released
                            try:
                                keyboard.release(eval(self.data.split('!')[1]))
                            except Exception as ex:
                                print(ex)
                        elif(self.data == 'SS'):
                            self.signal.serverStoped.emit(self.conn, self.id, self.serverPort)
                    else:
                        print("Header data value is not equal to received data length")
            except UnboundLocalError:
                pass
            except BlockingIOError:
                pass
            except IOError:
                pass
        self.conn.close()
        self.sendSocket.close()
        self.reciveSocket.close()
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', '---- | ' , "ReciveUserInput QRunnable terminated")
