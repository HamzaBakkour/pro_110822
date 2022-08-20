from PySide6 import QtCore, QtWidgets

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QScrollArea,
    QGridLayout
)

from scrollAreaTest3 import ScrollPanelWidget


import sys

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("pro_110822")
        self.setFixedSize(600, 800)
        self.mainLayout = QGridLayout()
        self.availableDevicesArea()
        # self.setCent(self.mainLayout)
        print("S")

    
    def availableDevicesArea(self):
        self.availableDevicesWidget = ScrollPanelWidget()
        self.mainLayout.addWidget(self.availableDevicesWidget)
        # self.availableDevicesWidget.show()
        print("S")
        

    




app = QApplication(sys.argv)
window = mainWindow()
window.show()
app.exec()