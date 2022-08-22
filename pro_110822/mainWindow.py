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
        #init the main window
        super(mainWindow, self).__init__(parent)
        self.setWindowTitle("pro_110822")
        self.setFixedSize(600, 800)

        #Set the main window widget
        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.layout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainWidget.layout)
        self.setCentralWidget(self.mainWidget)

        #Starting the main window with the firstOpenView view
        self.mainWindowView = firstOpenView()
        self.mainWidget.layout.addWidget(self.mainWindowView)
        self.mainWindowView.makeServerButton.clicked.connect(self.makeServer)


    def makeServer(self):
        self.mainWindowView.remove()
        self.mainWindowView = serverView()
        self.mainWidget.layout.addWidget(self.mainWindowView)
        print("Creating Server")
        return("Server")
 
# class mainWindowWidget(QtWidgets.QWidget):
#     def __init__(self, parent):        
#         super(mainWindowWidget, self).__init__(parent)
#         self.layout = QVBoxLayout(self)
#         self.setLayout(self.layout)
#         self.firstOpenView()
#         # self.serverView()


#     def firstOpenView(self):
#         view = firstOpenView()
#         self.layout.addWidget(view)




#     def connectedToServerView(self):
#         pass


app = QApplication([])
window = mainWindow()
window.show()
sys.exit(app.exec_())