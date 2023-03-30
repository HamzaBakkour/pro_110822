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
    def __init__(self, name: str, ip: list, port : int):        
        super(ClientWidget, self).__init__()

        self.ip = ip
        self.port = port
        self.layout = QGridLayout(self)
        self.setFixedHeight(75)
        self._init_ui(name, ip, port)
        self._set_style()

    def _set_style(self):
        self.setStyleSheet("QFrame {background-color: #c9c9c9;"
                            "border-width: 1px;"
                            "border-style: outset;"
                            "border-color: #787777;}"
                            "QLabel {background-color: #c9c9c9;"
                            "border: none;}"
                           )

    def _init_ui(self, clientName, clientIP, clientPort):
        leftGrid = QGridLayout()
        rightGrid = QGridLayout()

        self.layout.setSpacing(0)
        self.layout.setColumnStretch(0,3)
        self.layout.setColumnStretch(1,1)

        leftGrid.addWidget(QLabel('Client name : ' + clientName),0,0)
        # leftGrid.addWidget(QLabel('Shortcut: ' + shortcut), 1, 0)
        rightGrid.addWidget(QLabel('Client IP: ' + clientIP),0,0)
        rightGrid.addWidget(QLabel('Connected via: ' + str(clientPort)),1,0)


        self.layout.addLayout(leftGrid, 0, 0)
        self.layout.addLayout(rightGrid, 0, 1)








