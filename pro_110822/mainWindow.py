from PySide6 import QtCore, QtWidgets

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QScrollArea,
    QGridLayout,
    QVBoxLayout,
    QPushButton
)

from PySide6 import QtGui, QtCore, QtWidgets

from scrollAreaTest3 import scrollPanel


import sys

class mainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        self.setWindowTitle("pro_110822")
        self.setFixedSize(600, 800)
        self.form_widget = mainWindowWidgets(self) 
        self.setCentralWidget(self.form_widget) 



class mainWindowWidgets(QtWidgets.QWidget):

    def __init__(self, parent):        
        super(mainWindowWidgets, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.availableDevicesWidget = scrollPanel()
        self.connectedDevices = scrollPanel()

        self.layout.addWidget(self.availableDevicesWidget)
        self.layout.addWidget(self.connectedDevices)



        self.setLayout(self.layout)



app = QApplication([])
window = mainWindow()
window.show()
sys.exit(app.exec_())