from pro_110822_Logging_clss import Log

log = Log(8)

class Boo():
    def __init__(self) -> None:
        self.boo4()

    def boo1(self):
        log.info('printed the boo message')

    def boo2(self):
        log.error('this is error message')
        log.warning('this is warning')
        self.boo1()

    def boo3(self):
        log.critical('critical message')
        self.boo2()

    def boo4(self):
        log.debug('this is just a debug')
        self.boo3()


boo = Boo()

boo.boo4()