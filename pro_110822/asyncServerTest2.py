class MainWindow(QMainWindow):
    set_num = Signal(int, QColor)

    def __init__(self, rows, cols):
        super().__init__()
        self.setCentralWidget(widget_central)
        self.widget_outer_text = QLabel()
        self.widget_outer_text.setFont(font)
        self.set_num.connect(self.set_num_handler)
        

    @Slot(int, QColor)
    def set_num_handler(self, i, color):
        palette.setColor(QPalette.WindowText, color)
