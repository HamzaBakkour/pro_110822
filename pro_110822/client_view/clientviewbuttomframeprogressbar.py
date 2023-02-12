

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QRect



class ClientViewButtomFrameBrogressBar(QtWidgets.QProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_style()

    def _set_style(self):
        self.setStyleSheet(u"padding: 0px;")
        self.setValue(0)
        self.setTextVisible(False)

    def sizeHint(self):
        return QtCore.QSize(0, 0)