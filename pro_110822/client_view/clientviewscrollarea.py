import sys
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QApplication, QFormLayout, QScrollArea, QGridLayout, QPushButton
# import networkScanner

class ClientViewScrollArea(QScrollArea):

    def __init__(self, parent= None):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.scroll_panel = QtWidgets.QWidget()
        self.scroll_panel_layout = QFormLayout(self.scroll_panel)
        # self.scroll_panel_layout.setContentsMargins(0,0,0,0)
        # self.scroll_panel_layout.setVerticalSpacing(0)
        self.scroll_panel_layout.setHorizontalSpacing(0)
        # self.scroll_panel_layout.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scroll_panel_layout.setAlignment(QtCore.Qt.AlignTop)
        

        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidget(self.scroll_panel)

    def add_device(self, device: QtWidgets.QWidget):
        self.scroll_panel_layout.addWidget(device)
    
    def reseat(self):
        for i in reversed(range(self.scroll_panel_layout.count())): 
            self.scroll_panel_layout.itemAt(i).widget().deleteLater()
        pass


# import sys
# from PySide6 import QtGui, QtCore, QtWidgets
# from PySide6.QtWidgets import QApplication, QFormLayout, QScrollArea, QGridLayout, QPushButton
# # import networkScanner

# class ClientViewScrollArea(QScrollArea):

#     def __init__(self, *args, **kwargs):
#         super(ClientViewScrollArea, self).__init__(*args, **kwargs)
#         self._set_style()
#         self._init_ui()

#     def _set_style(self):
#         self.setStyleSheet(u"background-color: qlineargradient(spread:repeat, x1:1, y1:0, x2:1, y2:1, stop:0 rgba(184, 184, 184, 255),stop:1 rgba(209, 207, 207, 255));\n"
#                             "")
        
    
#     def _init_ui(self):
#         self.scroll_panel = QtWidgets.QWidget()
#         self.scroll_panel_layout = QFormLayout(self.scroll_panel)

#         self.setWidgetResizable(True)
#         self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
#         self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
#         self.setWidget(self.scroll_panel)

#     def add_device(self, device: QtWidgets.QWidget):
#         self.scroll_panel_layout.addWidget(device)
    
#     def reseat(self):
#         for i in reversed(range(self.scroll_panel_layout.count())): 
#             self.scroll_panel_layout.itemAt(i).widget().deleteLater()

