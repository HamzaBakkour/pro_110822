from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from pynput import mouse, keyboard#.mouse import Listener, Controller
import socket
import struct

import PySimpleGUI as sg

import sys
import os
import traceback
import logging
import time
import re

import pdb


class SendMouseKeyboard():
    def __init__(self):
        self.activeConnection = 0

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


    def start_listning(self):
        self.mouseListner = mouse.Listener(on_move=self._on_move, on_click=self._on_click, on_scroll=self._on_scroll)
        self.keyboardListner = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        self.mouseListner.start()
        self.keyboardListner.start()

        

  


