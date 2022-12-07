from pynput import mouse, keyboard#.mouse import Listener, Controller
import socket
import struct
import ctypes
import win32con
import win32api
import win32gui
import atexit




class SendMouseKeyboard():
    def __init__(self):
        self.activeConnection = None
        self.mouseListner = None
        self.keyboardListner = None
        self.supressing = 0
        self.savedCursors = False
        self.savedCursor1 = None
        self.savedCursor2 = None
        self.savedCursor3 = None
        self.savedCursor4 = None
        self.savedCursor5 = None
        self.savedCursor6 =None
        self.savedCursor7 = None
        self.savedCursor8 = None
        self.savedCursor9 = None
        self.savedCursor10 = None
        self.savedCursor11 = None
        self.savedCursor12 = None
        self.savedCursor13 = None
        self.savedCursor14 = None



    def _save_system_cursors(self):
        self.savedCursors = True
        sysCursor1 = win32gui.LoadImage(0, 32650, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED)
        sysCursor2 = win32gui.LoadImage(0, 32512, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED)
        sysCursor3 = win32gui.LoadImage(0, 32513, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED)
        sysCursor4 = win32gui.LoadImage(0, 32514, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED)
        sysCursor5 = win32gui.LoadImage(0, 32515, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED)
        sysCursor6 = win32gui.LoadImage(0, 32516, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED)
        sysCursor7 = win32gui.LoadImage(0, 32648, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED)
        sysCursor8 = win32gui.LoadImage(0, 32649, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED)
        sysCursor9 = win32gui.LoadImage(0, 32651, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED)
        sysCursor10 = win32gui.LoadImage(0, 32646, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED)
        sysCursor11 = win32gui.LoadImage(0, 32643, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED)
        sysCursor12 = win32gui.LoadImage(0, 32645, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED)
        sysCursor13 = win32gui.LoadImage(0, 32642, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED)
        sysCursor14 = win32gui.LoadImage(0, 32644, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED)

        self.savedCursor1 = ctypes.windll.user32.CopyImage(sysCursor1, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)
        self.savedCursor2 = ctypes.windll.user32.CopyImage(sysCursor2, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)
        self.savedCursor3 = ctypes.windll.user32.CopyImage(sysCursor3, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)
        self.savedCursor4 = ctypes.windll.user32.CopyImage(sysCursor4, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)
        self.savedCursor5 = ctypes.windll.user32.CopyImage(sysCursor5, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)
        self.savedCursor6 = ctypes.windll.user32.CopyImage(sysCursor6, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)
        self.savedCursor7 = ctypes.windll.user32.CopyImage(sysCursor7, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)
        self.savedCursor8 = ctypes.windll.user32.CopyImage(sysCursor8, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)
        self.savedCursor9 = ctypes.windll.user32.CopyImage(sysCursor9, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)
        self.savedCursor10 = ctypes.windll.user32.CopyImage(sysCursor10, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)
        self.savedCursor11 = ctypes.windll.user32.CopyImage(sysCursor11, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)
        self.savedCursor12 = ctypes.windll.user32.CopyImage(sysCursor12, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)
        self.savedCursor13 = ctypes.windll.user32.CopyImage(sysCursor13, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)
        self.savedCursor14 = ctypes.windll.user32.CopyImage(sysCursor14, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)


    def _restor_system_cursors(self):
        ctypes.windll.user32.SetSystemCursor(self.savedCursor1, 32650)
        ctypes.windll.user32.SetSystemCursor(self.savedCursor2, 32512)
        ctypes.windll.user32.SetSystemCursor(self.savedCursor3, 32513)
        ctypes.windll.user32.SetSystemCursor(self.savedCursor4, 32514)
        ctypes.windll.user32.SetSystemCursor(self.savedCursor5, 32515)
        ctypes.windll.user32.SetSystemCursor(self.savedCursor6, 32516)
        ctypes.windll.user32.SetSystemCursor(self.savedCursor7, 32648)
        ctypes.windll.user32.SetSystemCursor(self.savedCursor8, 32649)
        ctypes.windll.user32.SetSystemCursor(self.savedCursor9, 32651)
        ctypes.windll.user32.SetSystemCursor(self.savedCursor10, 32646)
        ctypes.windll.user32.SetSystemCursor(self.savedCursor11, 32643)
        ctypes.windll.user32.SetSystemCursor(self.savedCursor12, 32645)
        ctypes.windll.user32.SetSystemCursor(self.savedCursor13, 32642)
        ctypes.windll.user32.SetSystemCursor(self.savedCursor14, 32644)


        ctypes.windll.user32.DestroyCursor(self.savedCursor1)
        ctypes.windll.user32.DestroyCursor(self.savedCursor2)
        ctypes.windll.user32.DestroyCursor(self.savedCursor3)
        ctypes.windll.user32.DestroyCursor(self.savedCursor4)
        ctypes.windll.user32.DestroyCursor(self.savedCursor5)
        ctypes.windll.user32.DestroyCursor(self.savedCursor6)
        ctypes.windll.user32.DestroyCursor(self.savedCursor7)
        ctypes.windll.user32.DestroyCursor(self.savedCursor8)
        ctypes.windll.user32.DestroyCursor(self.savedCursor9)
        ctypes.windll.user32.DestroyCursor(self.savedCursor10)
        ctypes.windll.user32.DestroyCursor(self.savedCursor11)
        ctypes.windll.user32.DestroyCursor(self.savedCursor12)
        ctypes.windll.user32.DestroyCursor(self.savedCursor13)
        ctypes.windll.user32.DestroyCursor(self.savedCursor14)


    def _change_system_cursors(self, cursorFile : str):
        cursor1 = win32gui.LoadImage(0, cursorFile, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
        cursor2 = win32gui.LoadImage(0, cursorFile, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
        cursor3 = win32gui.LoadImage(0, cursorFile, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
        cursor4 = win32gui.LoadImage(0, cursorFile, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
        cursor5 = win32gui.LoadImage(0, cursorFile, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
        cursor6 = win32gui.LoadImage(0, cursorFile, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
        cursor7 = win32gui.LoadImage(0, cursorFile, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
        cursor8 = win32gui.LoadImage(0, cursorFile, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
        cursor9 = win32gui.LoadImage(0, cursorFile, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
        cursor10 = win32gui.LoadImage(0, cursorFile, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
        cursor11 = win32gui.LoadImage(0, cursorFile, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
        cursor12 = win32gui.LoadImage(0, cursorFile, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
        cursor13 = win32gui.LoadImage(0, cursorFile, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
        cursor14 = win32gui.LoadImage(0, cursorFile, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)


        ctypes.windll.user32.SetSystemCursor(cursor1, 32650)
        ctypes.windll.user32.SetSystemCursor(cursor2, 32512)
        ctypes.windll.user32.SetSystemCursor(cursor3, 32513)
        ctypes.windll.user32.SetSystemCursor(cursor4, 32514)
        ctypes.windll.user32.SetSystemCursor(cursor5, 32515)
        ctypes.windll.user32.SetSystemCursor(cursor6, 32516)
        ctypes.windll.user32.SetSystemCursor(cursor7, 32648)
        ctypes.windll.user32.SetSystemCursor(cursor8, 32649)
        ctypes.windll.user32.SetSystemCursor(cursor9, 32651)
        ctypes.windll.user32.SetSystemCursor(cursor10, 32646)
        ctypes.windll.user32.SetSystemCursor(cursor11, 32643)
        ctypes.windll.user32.SetSystemCursor(cursor12, 32645)
        ctypes.windll.user32.SetSystemCursor(cursor13, 32642)
        ctypes.windll.user32.SetSystemCursor(cursor14, 32644)       


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
        if(self.supressing == True):
            if (msg == 513 or msg == 514 or msg == 516 or msg == 517 or msg == 519 or msg == 520 or msg == 522):
                self.mouseListner._suppress = True
                print('supressing')
            else:
                self.mouseListner._suppress = False
        else:
            self.mouseListner._suppress = False


    def _keyboard_win32_event_filter(self, msg, data):
        print('msg: ', msg, ' data.vkCode: ', data.vkCode)
        if(self.supressing == True):
        # if (msg == 257 or msg == 256) and data.vkCode == 68:
        #     print("Supressing")
            self.keyboardListner._suppress = True
            print('supressing')
        else:
            self.keyboardListner._suppress = False


    def supressMnK(self, state : bool):
        if (state == True):
            self.supressing = True
            self._save_system_cursors()
            self._change_system_cursors("cursor.cur")
        elif (state == False):
            self.supressing = False
            if(self.savedCursors):
                self._restor_system_cursors()


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


        

  


