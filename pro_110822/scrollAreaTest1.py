import sys
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QApplication, QFormLayout, QScrollArea, QGridLayout, QPushButton


class ScrollPanelWidget(QtWidgets.QWidget):

    def __init__(self, parent= None):
        super(ScrollPanelWidget, self).__init__()
        self.initUI()
    
    def initUI(self):
        # formatting
        self.resize(550, 400)
        self.setWindowTitle("Scroll Panel Widget")

        # widgets
        self.scroll_panel = QtWidgets.QWidget()
        self.scroll_panel_layout = QFormLayout(self.scroll_panel)
        self.scroll_panel_layout.setContentsMargins(0,0,0,0)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.scroll_panel)

        # layout
        self.mainLayout = QGridLayout(self)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addWidget(self.scroll_area)


        for i in range(20):
            btn = QPushButton("test")
            self.scroll_panel_layout.addWidget(btn)


# Main
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ScrollPanelWidget()
    ex.show()
    sys.exit(app.exec_())