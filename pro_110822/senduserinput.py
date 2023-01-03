from pynput import mouse, keyboard
import functools
import subprocess
import struct
import socket
<<<<<<< HEAD
import os
import inspect
import ctypes
# import atexit
=======
import ctypes

>>>>>>> 43bdce52d15f5d21560d15852621038cbd08c8e3


def if_connected(func):
    @functools.wraps(func)
    def _wrapper(self, *args, **kwargs):
        if ((self.mouseListner.is_alive() or self.keyboardListner.is_alive()) and self.clientSocket):
            try:
                func(self, *args, **kwargs)
            except socket.error as error:
                if (error.errno == 10054):#[WinError 10054] An existing connection was forcibly closed by the remote host
                    self.stop_listning()
                    return
            except Exception as ex:
                print(ex)
    return _wrapper


class SendUserInput():
    def __init__(self):
        self.clientSocket = None
        self.mouseListner = None
        self.keyboardListner = None
        self.activeWin32Filter = False
        self.screenCovered = False
        self.coverScreenProcess = None
        self.screenWidth = self.get_screen_resulotion()[0]
        self.screenHight = self.get_screen_resulotion()[1]

<<<<<<< HEAD
    def get_screen_resulotion(self):
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return screensize
=======

    def set_active_connection(self, active)-> None:
            self.activeConnection = active
>>>>>>> 43bdce52d15f5d21560d15852621038cbd08c8e3

    def get_screen_resulotion(self):
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return screensize

    @if_connected
    def _on_move(self, x, y):
<<<<<<< HEAD
        message = f'M!{x/self.screenWidth}!{y/self.screenHight}'
        message = message.encode()
        header = struct.pack('<L', len(message))
        self.clientSocket.sendall(header + message)
=======
        if(self.mouseListner.is_alive() and self.activeConnection):
            message = f'M!{x/self.screenWidth}!{y/self.screenHight}'
            message = message.encode()
            header = struct.pack('<L', len(message))
            try:
                self.activeConnection.sendall(header + message)
            except socket.error as error:
                if (error.errno == 10054):#[WinError 10054] An existing connection was forcibly closed by the remote host
                    self.stop_listning()
                    return
            except Exception as ex:
                print("Exception raised while sending mouse movement to client.",
                f"Data header: {header}\n",
                f"Data: {message}\n",
                f"Sending socket: {self.activeConnection}\n\n",
                f"Exception:\n{ex}")

>>>>>>> 43bdce52d15f5d21560d15852621038cbd08c8e3

    @if_connected
    def _on_click(self, x, y, button, pressed):
        if pressed:
            message = f'P!{button}!1!{x}!{y}'
        else:
            message = f'P!{button}!0!{x}!{y}'
        message = message.encode()
        header = struct.pack('<L', len(message))
        self.clientSocket.sendall(header + message)


    @if_connected
    def _on_scroll(self, x, y, dx, dy):
        if dy < 0:
            message = f'S!d!{x}!{y}'
        else:
            message = f'S!u!{x}!{y}'
        message = message.encode()
        header = struct.pack('<L', len(message))
        self.clientSocket.sendall(header + message)


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
        self.clientSocket.sendall(header + message)


    @if_connected
    def _on_release(self, key):
        if (str(key)[0:3] == 'Key'):
            pass
        else:
            key = self.keyboardListner.canonical(key)
        message = f'R!{key}'
        message = message.encode()
        header = struct.pack('<L', len(message))
        self.clientSocket.sendall(header + message)


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
        if (supress == True and self.screenCovered == False):
            self.coverScreenProcess = subprocess.Popen(["py","-m","coverscreenalpha.py"])
            self.screenCovered = True
            self.activeWin32Filter = True
        elif (supress == False):
            self.activeWin32Filter = False
            if(self.screenCovered):
                self.coverScreenProcess.terminate()
                self.screenCovered = False


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


    def stop_listning(self):
        self.supress_user_input(False)
        self.mouseListner.stop()
        self.keyboardListner.stop()
        self.clientSocket = None
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} | ', f'{inspect.stack()[1][3]} || ', "LISTNINGSTOPED")


    def send_input_to_client(self, clientSocket)-> None:
        self.clientSocket = clientSocket
