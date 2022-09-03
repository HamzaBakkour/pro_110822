# from PySide6.QtCore import *
from PySide6.QtCore import QRunnable, QObject, Signal, Slot
from socketConnection import mouseAndKeyboardConnection

import sys
import os
import traceback
import logging
import time
import re

import socket
import datetime


class serverWorkerSignals(QObject):
    recivedConnection = Signal(object)

class listenForConnectionsWorker(QRunnable):
    def __init__(self, port: int)-> None:
        super(listenForConnectionsWorker, self).__init__()
        self.serverPort = port
        self.terminate = False

        self.signal = serverWorkerSignals()
        # self.serverConnection = mouseAndKeyboardConnection()
        # self.serverConnection.createSocket(None)
        # print("Server created.")

    @Slot()
    def run(self)-> int:
        s = socket.socket()    
        host = socket.gethostname() 
        port = 12345
        
        s.bind((host, port))  
        
        s.listen(5) 
                
        while True:
            c, addr = s.accept()       
            print ('got connection from addr', addr)
            date = datetime.datetime.now() 
            d = str(date)
            c.send(d.encode())     
            c.close()

        # print("Server listning for connection")
        # self.serverConnection.listenForConnections(self.serverPort)
        # while(self.terminate == False):
        #     try:
        #         self.serverConnection.s.accept()
        #         print("waiting for data")
        #         data = self.serverConnection.s.recv(1024)#
        #         print("listenForConnectionsWorker data: ", data)
        #         if(data):
        #             self.signal.recivedConnection.emit(data)
        #         else:
        #             self.signal.recivedConnection.emit(data)

        #     except: #Tryed to send data on something that is not a socket
        #         part1 = str(sys.exc_info())
        #         part2 = traceback.format_exc()
        #         origin = re.search(r'File(.*?)\,', part2).group(1) 
        #         loggMessage = origin + '\n' + part1  + '\n' + part2
        #         logging.info(loggMessage)
        
        # self.serverConnection.terminateSocket()
        # print("Server terminated")
        # return(1)