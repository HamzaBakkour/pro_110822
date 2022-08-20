from PySide6.QtWidgets import (
    QApplication,
    QMainWindow
) 

import sys

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("pro_110822")
        self.setFixedSize(600, 800)

    




app = QApplication(sys.argv)
window = mainWindow()
window.show()
app.exec()