#pro_110822/senduserinput.py
""" 
Send mouse and keyboard input over a socket connection.
"""

from pynput import mouse, keyboard
import datetime
import time
import pdb
import ctypes
from asyncio.exceptions import CancelledError
import queue
import ctypes
try:
    from prologging import Log
except ModuleNotFoundError:
    from pro_110822.prologging import Log



class SendUserInput():
    def __init__(self):
        self._mouse_listner = None
        self._keyboard_listner = None
        self._activeWin32Filter = False
        self._keyboard = keyboard.Controller()
        self._screen_width = self.get_screen_resulotion()[0]
        self._screen_hight = self.get_screen_resulotion()[1]
        self.events_queue = queue.Queue(maxsize=200)
        self._log = Log()
        self._keyboard_filter_encoded_list = []

    @staticmethod
    def get_screen_resulotion():
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        return screensize

    def _on_move(self, x, y):
        event = f'%!M!{x/self._screen_width}!{y/self._screen_hight}!&'
        if self.events_queue.full():
            return
        self.events_queue.put(event)

    def _on_click(self, x, y, button, pressed):
        if pressed:
            event = f'%!P!{button}!1!&'
        else:
            event = f'%!P!{button}!0!&'#!{x}!{y}
        if self.events_queue.full():
            return
        self.events_queue.put(event)

    def _on_scroll(self, x, y, dx, dy):
        if dy < 0:
            event = f'%!S!d!{x}!{y}!&'
        else:
            event = f'%!S!u!{x}!{y}!&'
        if self.events_queue.full():
            return
        self.events_queue.put(event)

    def _on_press(self, key):
        if (str(key)[0:3] != 'Key'):
            key = self._keyboard_listner.canonical(key)
        try:
            event = f'%!K!a!{key.char}!&'
        except AttributeError:
            event = f'%!K!s!{key}!&'
        if self.events_queue.full():
            return
        self.events_queue.put(event)

    def _on_release(self, key):
        if (str(key)[0:3] != 'Key'):
            key = self._keyboard_listner.canonical(key)
        event = f'%!R!{key}!&'
        if self.events_queue.full():
            return
        self.events_queue.put(event)

    def _pressed_long_enough(self):
        iteration = 0
        for this_el, next_el in zip(self._keyboard_filter_encoded_list, 
                                    self._keyboard_filter_encoded_list[1:]+ \
                                    [self._keyboard_filter_encoded_list[0]]):
            
            time = this_el.split('!')[1]
            now_h = int(time.split(':')[0])
            now_m = int(time.split(':')[1])
            now_s = time.split(':')[2]
            now_s = int(now_s.split('.')[0])
            now_mi = int(time.split('.')[1])

            time = next_el.split('!')[1]
            next_h = int(time.split(':')[0])
            next_m = int(time.split(':')[1])
            next_s = time.split(':')[2]
            next_s = int(next_s.split('.')[0])
            next_mi = int(time.split('.')[1])

            now = datetime.datetime(2002,2,2,now_h,now_m,now_s,now_mi)
            then = datetime.datetime(2002,2,2,next_h,next_m,next_s,next_mi)

            diff = then - now

            # self._log.debug(['_pressed_long_enough'],
            #                     message=f'diff:{diff}, len:{len(self._keyboard_filter_encoded_list)}')
            if diff.microseconds > 100000 :
                self._keyboard_filter_encoded_list = []
                return False
            iteration += 1
            if iteration == len(self._keyboard_filter_encoded_list) - 1:
                break
        if iteration > 60 :
            self._log.debug(['_pressed_long_enough'],
                                message=f'diff:{diff}, len:{len(self._keyboard_filter_encoded_list)}, LONG ENOUGH ->')
            self._keyboard_filter_encoded_list = []
            return True

    def _keyboard_win32_event_filter(self, msg, data):
        if data.scanCode == 60:
            now = datetime.datetime.now()
            self._keyboard_filter_encoded_list.append('60' + '!' + str(now.time()))#str(data.scanCode)
            if self._pressed_long_enough():
                self._log.info(['_keyboard_win32_event_filter'],
                               message="PRESSED LONG ENOUGH -> events_queue.put('X')")
                self.events_queue.put('X')
                time.sleep(1)

    def _mouse_win32_event_filter(self, msg, data):
            if (msg == 513 or msg == 514 or msg == 516 or msg == 517 or msg == 519 or msg == 520 or msg == 522):
                self._mouse_listner._suppress = True
            else:
                self._mouse_listner._suppress = False

    def start_listning(self):

        self._log.info(['start_listning'],
                       message='STARTED listning')

        self._mouse_listner = mouse.Listener(on_move=self._on_move,
        on_click = self._on_click,
        on_scroll = self._on_scroll,
        win32_event_filter= self._mouse_win32_event_filter,
        suppress=False        
        )

        self._keyboard_listner = keyboard.Listener(on_press=self._on_press,
         on_release=self._on_release,
         win32_event_filter = self._keyboard_win32_event_filter,
         suppress=True            
         )

        try:
            self._mouse_listner.start()
            self._keyboard_listner.start()
        except Exception as ex:
            self._log.error(['start_listning'],
                            message=f'{type(ex)} {ex}')

    def stop_listning(self):
        if (self._mouse_listner == None) or (self._keyboard_listner == None):
            self._log.info(['stop_listning'],
                           message='_mouse_listner/_keyboard_listner are None -> RETURNING')
            return

        self._log.info(['stop_listning'],
                       message='STOPPING mouse and keyboard listeners >')

        self._keyboard_listner.stop()
        self._mouse_listner.stop()

        self._log.info(['stop_listning'],
                       message='STOPPING mouse and keyboard listeners >>|')

        try:
            self._keyboard.press(keyboard.Key.ctrl_l)
            time.sleep(0.1)
            self._keyboard.release(keyboard.Key.ctrl_l)
        except Exception as ex:
            self._log.error(['stop_listning'],
                            message=f'at first exception, {type(ex)}, {ex}')
        try:
            self._keyboard.press(keyboard.Key.ctrl_r)
            time.sleep(0.1)
            self._keyboard.release(keyboard.Key.ctrl_r)
        except Exception as ex:
            self._log.error(['stop_listning'],
                            message=f'at second exception, {type(ex)}, {ex}')

        self._log.error(['stop_listning'],
                        message='DONE')


        self._keyboard_filter_encoded_list = []
