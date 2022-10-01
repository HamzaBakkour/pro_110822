from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QScrollArea,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QProgressBar,
    QProgressDialog
)


class ProgressBar(QtWidgets.QWidget):
    def __init__(self):        
        super(ProgressBar, self).__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10,0,10,0)
        # self.layout.setSpacing(0)


        self.setFixedSize(600, 20)

        self.pbar = QProgressBar(self)
        self.pbar.setAlignment(QtCore.Qt.AlignCenter)
        self.pbar.setFormat("")
        self.pbar.setValue(0)
        self.pbar.setGeometry(0,0,20,30)


        # self.txt = QLabel("asdasdasd asasdasdasdasdasddasdas asda sdasd asd asd as d")
        self.txt = QLabel("")
        self.txt.setGeometry(0,0,400,20)


        self.layout.addWidget(self.pbar)
        self.layout.addStretch(0)
        self.layout.addWidget(self.txt)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

    def value(self, value: int)-> None:
        self.pbar.setValue(value)

    def text(self, text: str)-> None:
        self.txt.setText(text)
        self.txt.adjustSize()

    def reseat(self):
        self.pbar.setValue(0)
        self.txt.setText(' ')

    def remove(self):
        self.deleteLater()