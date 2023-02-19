from PySide6.QtCore import QRunnable, QObject, Signal, Slot

import sys
import os
import traceback
import logging
import time
import re
import portscanner
import pdb
import inspect
# pdb.set_trace()
class SearchForServersWorkerSignals(QObject):
    foundServer = Signal(object, object, object)
    infoSignal = Signal(object, object)

class SearchForServersWorker(QRunnable):
    def __init__(self, port: int)-> None:
        super().__init__()
        self.signal = SearchForServersWorkerSignals()
        self.serverPort = port


    @Slot()
    def run(self)-> int:
        self.signal.infoSignal.emit(1 , 'Searching for servers...')
        scan = portscanner.port_scanner(self.serverPort, 50, 0.5)
        for entry in scan:
            self.signal.infoSignal.emit(int(float(entry['percentage'][:-1])) , entry['percentage'][:-4] + '%')
            if (len(entry['port_ok'])> 0):
                for address in entry['port_ok']:
                    self.signal.foundServer.emit('Unknown', address, self.serverPort)
            if int(float(entry['percentage'][:-1])) >= 100:
                self.signal.infoSignal.emit(100 , 'Search completed!')
                time.sleep(2)
                self.signal.infoSignal.emit(999 , ' ')
                self.signal.infoSignal.emit(0 , ' ')
        print(f'{os.path.basename(__file__)} | ', f'{inspect.stack()[0][3]} || ', "Search for server worker exiting!")
        return 1


