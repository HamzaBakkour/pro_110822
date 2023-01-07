#pro_110822/senduserinput.py
"""
Send mouse and keyboard input over a socket connection.

CLASS SendUserInput constins the following methods:
    - `__init__`
    - `get_screen_resulotion`
    - `_on_move`
    - `_on_click`
    - `_on_scroll`
    - `_on_press`
    - `_on_release`
    - `_keyboard_win32_event_filter`
    - `_mouse_win32_event_filter`
    - `supress_user_input`
    - `start_listning`
    - `stop_listning`
    - `send_input_to_client`
"""
from pynput import mouse, keyboard
import functools
import subprocess
import struct
import socket
import os
import inspect
import ctypes


import ctypes

def if_connected(func):
    """
    A wrapper to some of the SendUserInput methods.
    The wrapper checks if a valid connection is established before
    calling the wrapped function.
    """
    @functools.wraps(func)
    def _wrapper(self, *args, **kwargs):
        if ((self.mouseListner.is_alive() or self.keyboardListner.is_alive()) and self.activeConnection):
            try:
                func(self, *args, **kwargs)
            except socket.error as error:
                if (error.errno == 10054 or error.errno == 10053):
                    self._terminate_socket()
                    print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'socket errno {error} [Handeled]')
                    return
                else:
                    print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'socket errno {error} [Unhandeled]')
            except Exception as ex:
                print(ex)
    return _wrapper


class SendUserInput():
    def __init__(self):
        self.activeConnection = None
        self.mouseListner = None
        self.keyboardListner = None
        self.activeWin32Filter = False
        self.screenCovered = False
        self.coverScreenProcess = None
        self.keyBoard = keyboard.Controller()
        self.screenWidth = self.get_screen_resulotion()[0]
        self.screenHight = self.get_screen_resulotion()[1]


    def get_screen_resulotion(self):
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return screensize


    @if_connected
    def _on_move(self, x, y):
        message = f'M!{x/self.screenWidth}!{y/self.screenHight}'
        message = message.encode()
        header = struct.pack('<L', len(message))
        self.activeConnection.sendall(header + message)


    @if_connected
    def _on_click(self, x, y, button, pressed):
        if pressed:
            message = f'P!{button}!1!{x}!{y}'
        else:
            message = f'P!{button}!0!{x}!{y}'
        message = message.encode()
        header = struct.pack('<L', len(message))
        self.activeConnection.sendall(header + message)


    @if_connected
    def _on_scroll(self, x, y, dx, dy):
        if dy < 0:
            message = f'S!d!{x}!{y}'
        else:
            message = f'S!u!{x}!{y}'
        message = message.encode()
        header = struct.pack('<L', len(message))
        self.activeConnection.sendall(header + message)


    @if_connected
    def _on_press(self, key):
        if (str(key)[0:3] == 'Key'):
            pass
        else:
            key = self.keyboardListner.canonical(key)
        try:
            message = f'K!a!{key.char}'
        except AttributeError:
            message = f'K!s!{key}'
        message = message.encode()
        header = struct.pack('<L', len(message))
        self.activeConnection.sendall(header + message)


    @if_connected
    def _on_release(self, key):
        if (str(key)[0:3] == 'Key'):
            pass
        else:
            key = self.keyboardListner.canonical(key)
        message = f'R!{key}'
        message = message.encode()
        header = struct.pack('<L', len(message))
        self.activeConnection.sendall(header + message)


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


    def supress_user_input(self, supress : bool):
        """
        Calling this method will disable the mouse and keyboard input.
        """
        if (supress == True and self.screenCovered == False):
            self.coverScreenProcess = subprocess.Popen(["py","-m","coverscreenalpha.py"])
            self.screenCovered = True
            self.activeWin32Filter = True
        elif (supress == False):
            self.activeWin32Filter = False
            if(self.screenCovered):
                self.coverScreenProcess.kill()
                self.keyboardListner._suppress = False
                try:
                    self.keyBoard.press(keyboard.Key.ctrl_l)
                    self.keyBoard.release(keyboard.Key.ctrl_l)
                except Exception as ex:
                    print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Exceptions raisde, press ctrl_l\n{ex}')
                try:
                    self.keyBoard.press(keyboard.Key.ctrl_r)
                    self.keyBoard.release(keyboard.Key.ctrl_r)
                except:
                    print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Exceptions raisde, press ctrl_r\n{ex}')
                self.screenCovered = False


    def start_listning(self):
        """
        Start listning to the mouse and keyboard input.
        To send the input to a socket call the method send_input_to_client
        and provide a valid socket connection as an argument.
        """
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


    def _terminate_socket(self):
        try:
            self.activeConnection.close()
        except Exception as ex:
            print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', f'Exception raisd while terminating socket\n{self.activeConnection}\n{ex}')
        self.activeConnection = None
        self.supress_user_input(False)


    def stop_listning(self):
        """
        Stop listning to the mouse and keyboard input.
        """
        self.supress_user_input(False)
        self.mouseListner.stop()
        self.keyboardListner.stop()
        self.activeConnection = None
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "LISTNINGSTOPED")

    def send_input_to_client(self, clientSocket)-> None:
        self.activeConnection = clientSocket