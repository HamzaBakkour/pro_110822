from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
)

from PySide6 import QtGui

from random import randint

from PySide6 import QtCore

import sys

import time

class TransparentWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self._on = False
        self.setLayout(layout)
        self.setWindowOpacity(0.1)
        self.showFullScreen()
        self.setCursor(QtCore.Qt.BlankCursor)
        self.setStyleSheet("background-color: rgba(0, 255, 255, 90);")

    def show_window(self):
        if not self._on:
            self._on = True
            self.show()

    def hide_window(self):
        if self._on:
            self.hide()
            self._on = False


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.transparent_window = TransparentWindow()

        self.transparent_window.show_window()

        time.sleep(5)

        self.transparent_window.hide_window()


    def show_transparent_window(self):
        self.transparent_window.show_window()

    def hide_transparent_window(self):
        self.transparent_window.hide_window()


app = QApplication(sys.argv)
w = MainWindow()
w.show()


# w.show_transparent_window()

# time.sleep(5)

# w.hide_transparent_window()


app.exec_()











    # def __init__(self):
    #     super().__init__()
    #     self.cover_window = None  # No external window yet.
    #     cursor = QCursor(QtCore.Qt.BlankCursor)



 


    # def _show_cover_window(self):
    #     if self.cover_window is None:
    #         self.cover_window = AnotherWindow()
    #         self.cover_window.setWindowOpacity(0.1)
    #         self.cover_window.showFullScreen()
    #         self.cover_window.show()
    #         self.cover_window.setCursor(QtCore.Qt.BlankCursor)


    # def _close_cover_window(self):
    #     if self.cover_window is not None:
    #         self.cover_window.hide()  # Close window.
    #         self.cover_window = None  # Discard reference.
