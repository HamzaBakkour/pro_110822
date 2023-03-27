#pro_110822/senduserinput.py
""" 
Send mouse and keyboard input over a socket connection.
"""

from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from pynput import mouse, keyboard
import functools
import subprocess
from subprocess import PIPE, STDOUT
import struct
import socket
import os
import inspect
import ctypes
import queue
import time
import ctypes


class SendUserInputSignals(QObject):
    socketTerminated = Signal(object)


class SendUserInput():
    def __init__(self):
        self.activeConnection = None
        self.mouseListner = None
        self.keyboardListner = None
        self.activeWin32Filter = False
        self.screenCovered = False
        self.coverScreenProcess = None
        self.signal = SendUserInputSignals()
        self.keyBoard = keyboard.Controller()
        self.screenWidth = self.get_screen_resulotion()[0]
        self.screenHight = self.get_screen_resulotion()[1]
        self.events_queue = queue.Queue(maxsize=200)

    def get_screen_resulotion(self):
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return screensize

    def _on_move(self, x, y):
        event = f'M!{x/self.screenWidth}!{y/self.screenHight}'
        if self.events_queue.full():
            return
        self.events_queue.put(event)

    def _on_click(self, x, y, button, pressed):
        if pressed:
            event = f'P!{button}!1!{x}!{y}'
        else:
            event = f'P!{button}!0!{x}!{y}'
        if self.events_queue.full():
            return
        self.events_queue.put(event)

    def _on_scroll(self, x, y, dx, dy):
        if dy < 0:
            event = f'S!d!{x}!{y}'
        else:
            event = f'S!u!{x}!{y}'
        if self.events_queue.full():
            return
        self.events_queue.put(event)

    def _on_press(self, key):
        if (str(key)[0:3] != 'Key'):
            key = self.keyboardListner.canonical(key)
        try:
            event = f'K!a!{key.char}'
        except AttributeError:
            event = f'K!s!{key}'
        if self.events_queue.full():
            return
        self.events_queue.put(event)

    def _on_release(self, key):
        if (str(key)[0:3] != 'Key'):
            key = self.keyboardListner.canonical(key)
        event = f'R!{key}'
        if self.events_queue.full():
            return
        self.events_queue.put(event)

    def _keyboard_win32_event_filter(self, msg, data):
        if(self.activeWin32Filter):
            self.keyboardListner._suppress = True
        else:
            self.keyboardListner._suppress = False

    def _mouse_win32_event_filter(self, msg, data):
        if(self.activeWin32Filter):
            if (msg == 513 or msg == 514 or msg == 516 or msg == 517 or msg == 519 or msg == 520 or msg == 522):
                self.mouseListner._suppress = True
            else:
                self.mouseListner._suppress = False
        else:
            self.mouseListner._suppress = False

    def start_listning(self):
        self.mouseListner = mouse.Listener(on_move=self._on_move,
        on_click = self._on_click,
        on_scroll = self._on_scroll,
        win32_event_filter= self._mouse_win32_event_filter,
        suppress=False        
        )

        self.keyboardListner = keyboard.Listener(on_press=self._on_press,
         on_release=self._on_release,
         win32_event_filter = self._keyboard_win32_event_filter,
         suppress=False            
         )

        self.mouseListner.start()
        self.keyboardListner.start()
        print("listening STARTED")

    def stop_listning(self):
        self.mouseListner.stop()
        self.keyboardListner.stop()
        print("listening SOPED")










    # def supress_user_input(self, supress : bool)-> None:
    #     if (supress == True and self.screenCovered == False):
    #         screenCoverScriptpath = os.path.dirname(os.path.realpath(__file__)) 
    #         screenCoverScriptpath = screenCoverScriptpath + '\coverscreenalpha.py'
    #         self.coverScreenProcess = subprocess.Popen(["py",screenCoverScriptpath], stdout=PIPE, stderr=STDOUT)
    #         self.screenCovered = True
    #         self.activeWin32Filter = True
    #     elif (supress == False):
    #         self.activeWin32Filter = False
    #         if(self.screenCovered):
    #             self.coverScreenProcess.kill()
    #             self.keyboardListner._suppress = False
    #             try:
    #                 self.keyBoard.press(keyboard.Key.ctrl_l)
    #                 self.keyBoard.release(keyboard.Key.ctrl_l)
    #             except Exception as ex:
    #                 print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Exceptions raisde, press ctrl_l\n{ex}')
    #             try:
    #                 self.keyBoard.press(keyboard.Key.ctrl_r)
    #                 self.keyBoard.release(keyboard.Key.ctrl_r)
    #             except:
    #                 print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Exceptions raisde, press ctrl_r\n{ex}')
    #             self.screenCovered = False
