import unittest
from unittest.mock import patch
import time
from pynput.mouse import Controller as MC
from pynput.keyboard import Controller as KC
from pynput.keyboard import Key
import pdb


from pro_110822.server.senduserinput import SendUserInput


class TestSendUserInput(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        

    def test_start_stop_listener(self):
        sendinput = SendUserInput()
        sendinput.start_listning()
        time.sleep(0.1)
        self.assertTrue(sendinput._mouse_listner.running)
        self.assertTrue(sendinput._keyboard_listner.running)
        sendinput.stop_listning()
        time.sleep(0.1)
        self.assertFalse(sendinput._mouse_listner.running)
        self.assertFalse(sendinput._keyboard_listner.running)

    @patch('pro_110822.server.senduserinput.SendUserInput.get_screen_resulotion',
           return_value = (1, 1),
           autospec=True)
    def test_mouse_controller(self, screen_res):
        mouse = MC()
        sendinput = SendUserInput()
        sendinput.start_listning()
        time.sleep(0.1)
        mouse.move(1,-1)
        sendinput.stop_listning()
        self.assertGreater(len(sendinput.events_queue.queue),
                           0)
        
        movement_recorded = False
        for entry in sendinput.events_queue.queue:
            elements = entry.split('!')
            if elements[1] == 'M':
                movement_recorded = True
                self.assertEqual(len(elements),
                                5)

                self.assertEqual(elements[0],
                                '%')
                self.assertEqual(elements[1],
                                'M')
                self.assertEqual(elements[4],
                                '&')
                try:
                    _ = float(elements[2])
                    _ = float(elements[3])
                except Exception as ex:
                    self.fail(f'{type(ex)}, {ex}'\
                            '\nMouse position elements at index 2 and/or 3 are not float')
                    
        self.assertTrue(movement_recorded,
                        f'{sendinput.events_queue.queue}\n'\
                            'None of the events in the envent queue are mouse movement.')

    def test_keyboard_controller(self):
        keyboard = KC()
        sendinput = SendUserInput()
        sendinput.start_listning()
        time.sleep(0.1)
        keyboard.press(Key.f3)
        keyboard.release(Key.f3)
        sendinput.stop_listning()
        self.assertGreater(len(sendinput.events_queue.queue),
                           1)
        
        key_recorded = 0
        for entry in sendinput.events_queue.queue:
            elements = entry.split('!')
            if (elements[1] == 'K') and (elements[3] == 'Key.f3'):
                key_recorded += 1
                self.assertEqual(len(elements),
                                5)

                self.assertEqual(elements[0],
                                '%')
                self.assertEqual(elements[1],
                                'K')
                self.assertEqual(elements[2],
                                's')
                self.assertEqual(elements[3],
                                'Key.f3')
                self.assertEqual(elements[4],
                                '&')
                
            if (elements[1] == 'R') and (elements[2] == 'Key.f3'):
                key_recorded += 1
                self.assertEqual(len(elements),
                                4)

                self.assertEqual(elements[0],
                                '%')
                self.assertEqual(elements[1],
                                'R')
                self.assertEqual(elements[2],
                                'Key.f3')
                self.assertEqual(elements[3],
                                '&')
                  
        self.assertGreater(key_recorded,
                           1)
