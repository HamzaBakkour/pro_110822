#pro_110822/senduserinput.py
""" 
Send mouse and keyboard input over a socket connection.
"""

from pynput import mouse, keyboard
import datetime
import pdb
import ctypes
import queue
import ctypes
from prologging import Log


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
            event = f'%!P!{button}!1!{x}!{y}!&'
        else:
            event = f'%!P!{button}!0!{x}!{y}!&'
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

    def _keyboard_filter_encoded_algorithm(self):
        tick = 0
        pingo = False
        pingo_list = []
        # print('-----------------------------------------------')
        # print(f'self._keyboard_filter_encoded_list:{self._keyboard_filter_encoded_list}')
        # print('-----------------------------------------------')

        for el in self._keyboard_filter_encoded_list:
            if (el.split('!')[0] == '29') and (tick == 0):
                tick += 1
            elif (el.split('!')[0] == '29') and (tick == 1):
                continue
            elif (el.split('!')[0] == '50') and (tick == 1):
                tick += 1
            elif (el.split('!')[0] == '50') and (tick == 2):
                continue
            elif (el.split('!')[0] == '2') and (tick == 2):
                tick += 1
            elif (el.split('!')[0] != '29') or (el.split('!')[0] == '50') or (el.split('!')[0] == '2'):
                self._keyboard_filter_encoded_list = []
            elif (el.split('!')[0] == '29') and (tick == 2):
                self._keyboard_filter_encoded_list = []
        if (tick == 3):
            pingo_list = self._keyboard_filter_encoded_list
            self._keyboard_filter_encoded_list = []
            pingo = True


        if pingo :
            self._log.info(['_keyboard_filter_encoded_algorithm'],
                      message='!!!BINGO!!!')
            def is_it_real_pingo(pingo_):
                iteration = 0
                for this_el, next_el in zip(pingo_, pingo_[1:]+[pingo_[0]]):
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
                    self._log.debug(['_keyboard_filter_encoded_algorithm',
                                     'is_it_real_pingo'],
                                     message=f'diff:{diff}')
                    print(f'diff:{diff}')
                    if diff.seconds > 2 : #or diff.microseconds > 500000
                        return False
                    iteration += 1
                    if iteration == len(pingo_) - 1:
                        break
                return True
            if is_it_real_pingo(pingo_list):
                self._log.info(['_keyboard_filter_encoded_algorithm'],
                               message='REAL BINGO -> unsupress_user_input')
                self.unsupress_user_input()
            else:
                self._log.info(['_keyboard_filter_encoded_algorithm'],
                               message='FALSE BINGO ->...')          

    def _keyboard_win32_event_filter(self, msg, data):

        if(self._activeWin32Filter):
            try:
                self._keyboard_listner._suppress = True
            except AttributeError:
                if self._keyboard_listner == None:
                    self._log.error(['_keyboard_win32_event_filter'],
                                   message='trying to supress None listner -> RETURNING')
                    return
                else:
                    raise AttributeError
            now = datetime.datetime.now()
            self._keyboard_filter_encoded_list.append(str(data.scanCode) + '!' + str(now.time()))
            self._keyboard_filter_encoded_algorithm()
        else:
            self._keyboard_listner._suppress = False

    def _mouse_win32_event_filter(self, msg, data):
        if(self._activeWin32Filter):
            if (msg == 513 or msg == 514 or msg == 516 or msg == 517 or msg == 519 or msg == 520 or msg == 522):
                self._mouse_listner._suppress = True
            else:
                self._mouse_listner._suppress = False
        else:
            self._mouse_listner._suppress = False

    def supress_user_input(self)-> None:
        self._log.info(['supress_user_input'],
                       message='SUPRESSING user input...')
        self._activeWin32Filter = True

    def unsupress_user_input(self)-> None:
        self._log.info(['unsupress_user_input'],
                       message='UNSUPRESSING user input')
        if self._keyboard_listner == None:
            self._activeWin32Filter = False
            return

        self.stop_listning()

        try:
            self._keyboard.press(keyboard.Key.ctrl_l)
            self._keyboard.release(keyboard.Key.ctrl_l)
        except Exception as ex:
            self._log.error(['unsupress_user_input'],
                            message=f'at first exception, {type(ex)}, {ex}')
        try:
            self._keyboard.press(keyboard.Key.ctrl_r)
            self._keyboard.release(keyboard.Key.ctrl_r)
        except Exception as ex:
            self._log.error(['unsupress_user_input'],
                            message=f'at second exception, {type(ex)}, {ex}')

    def start_listning(self):
        self._mouse_listner = mouse.Listener(on_move=self._on_move,
        on_click = self._on_click,
        on_scroll = self._on_scroll,
        win32_event_filter= self._mouse_win32_event_filter,
        suppress=False        
        )

        self._keyboard_listner = keyboard.Listener(on_press=self._on_press,
         on_release=self._on_release,
         win32_event_filter = self._keyboard_win32_event_filter,
         suppress=False            
         )

        self._mouse_listner.start()
        self._keyboard_listner.start()
        print("\nsendunserinput, start_listning, listening STARTED")

    def stop_listning(self):
        if self._mouse_listner == None:
            return
        
        self._mouse_listner.stop()
        self._keyboard_listner.stop()
        self._mouse_listner = None
        self._keyboard_listner = None
        self._keyboard_filter_encoded_list = []
        self._log.info(['stop_listning'],
                       message='listening STOPPED, _mouse_listner, _keyboard_listner set to None')
        # print("\nsendunserinput, stop_listning, listening STOPPED")











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
