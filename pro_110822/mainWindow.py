from PySide6 import QtCore, QtWidgets

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QScrollArea,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel
)

from PySide6 import QtGui, QtCore, QtWidgets

from scrollArea import scrollPanel

from firstOpenView import firstOpenView
from serverView import serverView

import sys

class mainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        self.setWindowTitle("pro_110822")
        self.setFixedSize(600, 800)
        self.mainWidget = mainWindowWidget(self)
        self.setCentralWidget(self.mainWidget)


 
class mainWindowWidget(QtWidgets.QWidget):
    def __init__(self, parent):        
        super(mainWindowWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.firstOpenView()
        # self.serverView()


    def firstOpenView(self):
        view = firstOpenView()
        self.layout.addWidget(view)


    def serverView(self):
        view = serverView()
        self.layout.addWidget(view)


    def connectedToServerView(self):
        pass


app = QApplication([])
window = mainWindow()
window.show()
sys.exit(app.exec_())