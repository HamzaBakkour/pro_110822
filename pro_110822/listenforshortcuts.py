from pynput import keyboard
from multiprocessing.connection import Client
import sys
import time

class ListenForShortcuts():
    def __init__(self, addr: str, port: int)-> None:
        self.address = (addr, port)#5001
        self.listner = False
        self._connect()

    def _on_activate(self, m):
        self.conn.send(m)
        print('sent -> ', m)

    def _connect(self):
        self.conn = Client(self.address, authkey=b'pro110822')

    def define_shortcuts(self, *args):

        def _get_count_of_shortcuts():
            n = 0
            for _ in args:
                n = n + 1
            return n

        count = _get_count_of_shortcuts()

        self.argg = '{'
        for _ in range(count):
            self.argg = self.argg + "'" + args[_] + "'" + ':' + ' lambda self = self: self._on_activate({})'.format("'" + args[_] + "'") + ', '
        self.argg = self.argg[:-2] + '}'
        print(f'argg : {self.argg}')

        if self.listner:
            print("stoped")
            self.listner.stop()
            self.listner =  keyboard.GlobalHotKeys(eval(self.argg))
            self.listner.start()
            print("stoped exit")
        else:
            print("started")
            self.listner =  keyboard.GlobalHotKeys(eval(self.argg))
            self.listner.start()
            print("started exit")

# test = ListenForShortcuts('localhost', 5001)

# test.define_shortcuts('<ctrl>+m+1', '<ctrl>+m+2')

# time.sleep(10)

# print("333333333333333333333333333333333333")

# test.define_shortcuts('<ctrl>+m+3')

# time.sleep(20)
