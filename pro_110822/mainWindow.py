from PySide6 import QtCore, QtWidgets

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QScrollArea,
    QGridLayout,
    QVBoxLayout,
    QPushButton,
    QLabel
)

from PySide6 import QtGui, QtCore, QtWidgets

from scrollArea import scrollPanel

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

        self.availableDevicesWidget = scrollPanel()
        self.connectedDevices = scrollPanel()

        self.layout.addWidget(QLabel("Available devices"))
        self.layout.addWidget(self.availableDevicesWidget)
        self.availableDevicesWidget.showAvaialableDevices()


        self.layout.addWidget(QLabel("Connected devices"))
        self.layout.addWidget(self.connectedDevices)

        self.setLayout(self.layout)



app = QApplication([])
window = mainWindow()
window.show()
sys.exit(app.exec_())