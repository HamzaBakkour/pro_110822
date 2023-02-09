
from PySide6.QtWidgets import  QSizePolicy
from . import clientviewupperframebtn1





class ClientViewUpperFrameBtn2(clientviewupperframebtn1.ClientViewUpperFrameBtn1):

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
                                        "       background-color: #0279f0;\n"
                                        "       border: 1px solid #0279f0;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton::pressed\n"
                                        "{\n"
                                        "       background-color: #2590fa;\n"
                                        "       border: 1px solid #2590fa;\n"
                                        "}\n"
                                        "")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFlat(False)
