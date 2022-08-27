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


class progressBar(QtWidgets.QWidget):
    def __init__(self):        
        super(progressBar, self).__init__()
        self.layout = QHBoxLayout(self)


        self.setFixedSize(600, 38)

        self.pbar = QProgressBar(self)
        self.pbar.setAlignment(QtCore.Qt.AlignCenter)
        self.pbar.setFormat("")
        self.pbar.setValue(20)


        self.txt = QLabel("asdasdasd asasdasdasdasdasddasdas asda sdasd asd asd as d")
        # self.txt = QLabel("")


        self.layout.addWidget(self.pbar)
        self.layout.addStretch(0)
        self.layout.addWidget(self.txt)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

    def pbarValue(self, value: int)-> None:
        self.pbar.setValue(value)

    def pbarText(self, text: str)-> None:
        self.txt.setText(text)

    def pbarReseat(self):
        self.pbar.setValue(0)
        self.txt.setText('')

    def remove(self):
        self.deleteLater()