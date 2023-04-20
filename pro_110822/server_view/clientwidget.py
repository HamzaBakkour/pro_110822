from PySide6 import QtCore, QtWidgets

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QScrollArea,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel
)

class ClientWidget(QtWidgets.QFrame):
    def __init__(self, client):        
        super(ClientWidget, self).__init__()
        print(f'\nClientWidget, __init__, recived client:{client}')
        self.ip = client[0][0]
        self.port = client[0][1]
        self.name = client[1]
        self.resolution = client[2]
        self.layout = QGridLayout(self)
        self.setFixedHeight(75)
        self._init_ui()
        self._set_style()

    def _set_style(self):
        self.setStyleSheet("QFrame {background-color: #c9c9c9;"
                            "border-width: 1px;"
                            "border-style: outset;"
                            "border-color: #787777;}"
                            "QLabel {background-color: #c9c9c9;"
                            "border: none;}"
                           )

    def _init_ui(self):
        leftGrid = QGridLayout()
        rightGrid = QGridLayout()

        self.layout.setSpacing(0)
        self.layout.setColumnStretch(0,3)
        self.layout.setColumnStretch(1,1)

        leftGrid.addWidget(QLabel('Client name : ' + self.name),0,0)
        # leftGrid.addWidget(QLabel('Shortcut: ' + shortcut), 1, 0)
        rightGrid.addWidget(QLabel('Client IP: ' +  self.ip),0,0)
        rightGrid.addWidget(QLabel('Connected via: ' + str(self.port)),1,0)


        self.layout.addLayout(leftGrid, 0, 0)
        self.layout.addLayout(rightGrid, 0, 1)








