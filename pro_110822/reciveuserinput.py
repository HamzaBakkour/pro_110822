from PySide6.QtCore import QRunnable, Slot

from pynput.mouse import Controller as MC
from pynput.mouse import Button

from pynput.keyboard import Controller as KC
from pynput.keyboard import Key

import socket
import platform
import ctypes
import struct


class ReciveUserInput(QRunnable):
    def __init__(self, serverIP: str, serverPort: str)-> None:
        super(ReciveUserInput, self).__init__()
        self.serverIP = serverIP
        self.serverPort = int(serverPort)

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
        sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        reciveSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        reciveSocket.bind(('',0))

        sendSocket.connect((self.serverIP, self.serverPort))

        screenRez = self.get_screen_resulotion()
        receiveSocetPort = reciveSocket.getsockname()[1]

        message = "C!{}!{}!{}!{}".format(screenRez[0], screenRez[1], receiveSocetPort, self.get_pc_name())
        message = message.encode()
        header = struct.pack('<L', len(message))

        try:
            sendSocket.sendall(header + message)
        except Exception as e:
            print(str(e))

        reciveSocket.listen(5)
        self.conn, address = reciveSocket.accept()
        print("from receive worker accepted {} {}".format(self.conn, address))

        mouse = MC()
        keyboard = KC()

        while(True):
            try:
                headerData = self.receive_n_bytes(4)
                if (len(headerData) == 4):
                    dataLen = struct.unpack('<L', headerData)[0]
                    data = self.receive_n_bytes(dataLen)
                    if len(data) == dataLen:
                        data = data.decode()
                        # print(f'>{data}')
                        if (data.split('!')[0] == 'M'):
                            mouse.position = (int((float(data.split('!')[1])*screenRez[0])), int((float(data.split('!')[2])*screenRez[1])))
                        elif (data.split('!')[0] == 'P'):
                            if (data.split('!')[2] == '1'):
                                mouse.press(eval(data.split('!')[1]))
                            elif (data.split('!')[2] == '0'):
                                mouse.release(eval(data.split('!')[1]))
                        elif (data.split('!')[0] == 'K'):
                            # print('P data', data)
                            # print('data 4:7', data[4:7])
                            try:
                                if (data[4:7] == 'Key'):
                                    # print('Key')
                                    keyboard.press(eval(data.split('!')[2]))
                                else:
                                    keyboard.press(data.split('!')[2])
                            except Exception as ex:
                                print(ex)
                        elif (data.split('!')[0] == 'R'):
                            # print('R data', data)
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
