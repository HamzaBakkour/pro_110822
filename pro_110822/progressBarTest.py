import sys
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QProgressBar

class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(10, 10, 100, 10)
        self.pbar.setValue(95)
        
        self.setWindowTitle("QT Progressbar Example")
        self.setGeometry(32,32,320,200)
        self.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.handleTimer)
        self.timer.start(1000)

    def handleTimer(self):
        value = self.pbar.value()
        if value < 100:
            value = value + 1
            self.pbar.setValue(value)
        else:
            self.timer.stop()
            self.pbar.setValue(95)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())