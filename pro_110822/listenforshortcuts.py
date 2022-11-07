from pynput import keyboard
from multiprocessing.connection import Client
import sys
import time

class ListenForShortcuts():
    def __init__(self, addr: str, port: int)-> None:
        self.address = (addr, port)#5001

    def connect(self):
        self.conn = Client(self.address, authkey=b'pro110822')

    def on_activate(self, m):
        self.conn.send(m)
        print('sent -> ', m)

    def terminate(self):
        sys.exit()

    def start_listning(self):
        self.connect()

        msg = self.conn.recv()
        print('received <-', msg)

        argumentsList = []
        numberOfShortcuts = int(msg.split('!')[1])
        for i in range(0,numberOfShortcuts):
            argumentsList.append("'" + msg.split('!')[i + 2] + "'")

        argg = '{'
        for i in range(0,numberOfShortcuts):
            argg = argg + argumentsList[i] + ':' + ' lambda: self.on_activate({})'.format(argumentsList[i]) + ', '
        argg = argg[:-2] + '}'
        print(argg)

        shortcut =  keyboard.GlobalHotKeys(eval(argg))
        shortcut.start()

        while(1):
            msg = self.conn.recv()
            if msg == "TR":
                self.terminate()