#pro_110822/firstOpenView.py
"""
The programs main window module

CLASS firstOpenView constins the following methods:
    - `__init__`
    - `setUpperFrame`
    - `setAvailableServersArea`
    - `addDevice`
"""

from PySide6 import QtCore, QtWidgets

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QScrollArea,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel
)

from scrollArea import scrollPanel


class firstOpenView(QtWidgets.QWidget):
    """
    First open view is a supclass of `PySide6.QtWidgets.QWidget`.  
    This is the first dispalyed view when the program is started.  
    <pre>

    ------------------------------------------------------------  
    |                                        [make server]     |  
    |Available servers                       [Refresh]         |  
    |----------------------------------------------------------|  
    |Server name                                               |  
    |Server IP                                  [Connect]      |  
    |                                                          |  
    |                                                          |  
    |                                                          |  
    |                                                          |  
    |                                                          |  
    |                                                          |  
    |                                                          |  
    |                                                          |  
    |                                                          |  
    |                                                          |  
    |                                                          |  
    |                                                          |  
    |                                                          |  
    |                                                          |  
    |                                                          |  
    |                                                          |  
    |                                                          |  
    |                                                          |  
    ------------------------------------------------------------  

    </pre>
    """
    def __init__(self):
        """
        Constructor method.  
        Initiate the first open view.  
        """
        super(firstOpenView, self).__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10,30,10,0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.setUpperFrame()
        self.setAvailableServersArea()


    def setUpperFrame(self):
        """
        <pre>

        ------------------------------------------------------------
        |                                        [make server]     |
        |Available servers                       [Refresh]         |
        |----------------------------------------------------------|

        </pre>
        """
        self.upperFrameLayout = QHBoxLayout()
        self.upperFrameLayout.addWidget(QLabel("Available servers"))

        self.makeServerButton = QPushButton("Make Server")
        self.makeServerButton.setCheckable(True)
        self.refreshButton = QPushButton("Refresh")
        self.refreshButton.setCheckable(True)

        self.upperFrameLayout.addWidget(self.makeServerButton)
        self.upperFrameLayout.addWidget(self.refreshButton)
        self.layout.addLayout(self.upperFrameLayout)



    def setAvailableServersArea(self):
        """
        Available servers area is an instance of the class `scrollPaneel`  
        
        <pre>

        |----------------------------------------------------------|
        |Server name                                               |
        |Server IP                                  [Connect]      |
        |                                                          |
        |                                                          |
        |                                                          |
        |                                                          |
        |                                                          |
        |                                                          |
        |                                                          |
        |                                                          |
        |                                                          |
        |                                                          |
        |                                                          |
        |                                                          |
        |                                                          |
        |                                                          |
        |                                                          |
        |                                                          |
        |                                                          |
        |                                                          |
        ------------------------------------------------------------

        </pre>
        """
        self.availableServers = scrollPanel()
        self.layout.addWidget(self.availableServers)

    def addDeivce(self, device: QtWidgets.QWidget):
        """
        <pre>

        |----------------------------------------------------------|
        |Server name                                               |
        |Server IP                                  [Connect]      |

        </pre>
          
        Discovered servers on the local network will be added to the  
        first open view.  
        The user can click the `Connect` button to connect to the server.  
        """
        self.availableServers.addDevice(device)


    def remove(self):
        """
        Delete the first open view widget.
        """
        self.deleteLater()
