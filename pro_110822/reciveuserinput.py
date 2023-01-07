from PySide6.QtCore import QRunnable, Slot

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


class ReciveUserInput(QRunnable):
    def __init__(self, serverIP: str, serverPort: str)-> None:
        super(ReciveUserInput, self).__init__()
        self.serverIP = serverIP
        self.serverPort = int(serverPort)
        self.alive = True
        self.sendSocket = None
        self.reciveSocket = None

    def get_screen_resulotion(self):
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return screensize

    @staticmethod
    def get_pc_name():
        return platform.node()


    def receive_n_bytes(self, n):
        """ Convenience method for receiving exactly n bytes from
            self.socket (assuming it's open and connected).
        """
        data = ''.encode()
        while len(data) < n:
            chunk = self.conn.recv(n - len(data))
            if ((chunk == ''.encode())):
                break
            data += chunk
        return data


    @Slot()
    def run(self)-> int:
        self.sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.reciveSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.reciveSocket.bind(('',0))
        self.reciveSocket.setblocking(0)


        self.sendSocket.connect((self.serverIP, self.serverPort))

        screenRez = self.get_screen_resulotion()
        receiveSocetPort = self.reciveSocket.getsockname()[1]

        message = "C!{}!{}!{}!{}".format(screenRez[0], screenRez[1], receiveSocetPort, self.get_pc_name())
        message = message.encode()
        header = struct.pack('<L', len(message))

        try:
            self.sendSocket.sendall(header + message)
        except Exception as e:
            print(str(e))

        
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
                headerData = self.receive_n_bytes(4)
                if (len(headerData) == 4):
                    dataLen = struct.unpack('<L', headerData)[0]
                    data = self.receive_n_bytes(dataLen)
                    if len(data) == dataLen:
                        data = data.decode()
                        if (data.split('!')[0] == 'M'):
                            mouse.position = (int((float(data.split('!')[1])*screenRez[0])), int((float(data.split('!')[2])*screenRez[1])))
                        elif (data.split('!')[0] == 'P'):
                            if (data.split('!')[2] == '1'):
                                mouse.press(eval(data.split('!')[1]))
                            elif (data.split('!')[2] == '0'):
                                mouse.release(eval(data.split('!')[1]))
                        elif (data.split('!')[0] == 'K'):

                            try:
                                if (data[4:7] == 'Key'):
                                    keyboard.press(eval(data.split('!')[2]))
                                else:
                                    keyboard.press(data.split('!')[2])
                            except Exception as ex:
                                print(ex)
                        elif (data.split('!')[0] == 'R'):
                            try:
                                keyboard.release(eval(data.split('!')[1]))
                            except Exception as ex:
                                print(ex)

                    else:
                        print("Header data value is not equal to received data length")
            except UnboundLocalError:
                pass
            except BlockingIOError:
                pass
            except IOError:
                pass
        self.sendSocket.close()
        self.reciveSocket.close()
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', '---- | ' , "ReciveUserInput QRunnable terminated")
