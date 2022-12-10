from pynput import mouse, keyboard
import subprocess
import struct
import atexit

class SendMouseKeyboard():
    def __init__(self):
        self.activeConnection = None
        self.mouseListner = None
        self.keyboardListner = None
        self.activeWin32Filter = False
        self.screenCovered = False
        self.coverScreenProcess = None
        atexit.register(self.stop_listning)


    def set_active_connection(self, active)-> None:
            self.activeConnection = active


    def _on_move(self, x, y):
        message = f'M!{x}!{y}'
        message = message.encode()
        header = struct.pack('<L', len(message))
        try:
            self.activeConnection.sendall(header + message)
        except Exception as e:
            # print(str(e))
            pass


    def _on_click(self, x, y, button, pressed):
        if pressed:
            message = f'P!{button}!1!{x}!{y}'
        else:
            message = f'P!{button}!0!{x}!{y}'
        message = message.encode()
        header = struct.pack('<L', len(message))
        try:
            self.activeConnection.sendall(header + message)
        except Exception as e:
            # print(str(e))
            pass


    def _on_scroll(self, x, y, dx, dy):
        if dy < 0:
            message = f'S!d!{x}!{y}'
        else:
            message = f'S!u!{x}!{y}'
        message = message.encode()
        header = struct.pack('<L', len(message))
        try:
            self.activeConnection.sendall(header + message)
        except Exception as e:
            # print(str(e))
            pass


    def _on_press(self, key):
        try:
            message = f'K!a!{key.char}'
        except AttributeError:
            message = f'K!s!{key}'
        message = message.encode()
        header = struct.pack('<L', len(message))
        try:
            self.activeConnection.sendall(header + message)
        except Exception as e:
            # print(str(e))
            pass


    def _on_release(self, key):  
        message = f'R!{key}'
        message = message.encode()
        header = struct.pack('<L', len(message))
        try:
            self.activeConnection.sendall(header + message)
        except Exception as e:
            # print(str(e))
            pass


    def _mouse_win32_event_filter(self, msg, data):
        # print('msg: ', msg, ' data: ', data)
        if(self.activeWin32Filter == True):
            if (msg == 513 or msg == 514 or msg == 516 or msg == 517 or msg == 519 or msg == 520 or msg == 522):#
                self.mouseListner._suppress = True
            else:
                self.mouseListner._suppress = False
        else:
            self.mouseListner._suppress = False


    def _keyboard_win32_event_filter(self, msg, data):
        # print('msg: ', msg, ' data.vkCode: ', data.vkCode)
        if(self.activeWin32Filter == True):
            self.keyboardListner._suppress = True
        else:
            self.keyboardListner._suppress = False


    def supressMnK(self, supress : bool):
        if (supress == True and self.screenCovered == False):
            self.coverScreenProcess = subprocess.Popen(["py","-m","coverscreenalpha.py"])
            self.screenCovered = True
            self.activeWin32Filter = True

        elif (supress == False):
            self.activeWin32Filter = False
            if(self.screenCovered == True):
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
            self.mouseListner._suppress = False
            self.keyboardListner._suppress = False
            self.mouseListner.stop()
            self.keyboardListner.stop()
            print("LISTNINGSTOPED")