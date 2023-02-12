from client_view import clientviewupperframebtn1
from PySide6.QtWidgets import QSizePolicy


class ServerViewUpperFrameBtn1(clientviewupperframebtn1.ClientViewUpperFrameBtn1):

    def _set_style(self):
        self.setStyleSheet(u"QPushButton::flat\n"
                            "{\n"
                            "       background-color: transparent;\n"
                            "       border: none;\n"
                            "       color: #fff;\n"
                            "}\n"
                            "\n"
                            "QPushButton::hover\n"
                            "{\n"
                            "       background-color: #fc1c03;\n"
                            "       border: 1px solid #fc1c03;\n"
                            "}\n"
                            "\n"
                            "QPushButton::pressed\n"
                            "{\n"
                            "       background-color: #fa5c4b;\n"
                            "       border: 1px solid #fa5c4b;\n"
                            "}\n"
                            "")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFlat(False)