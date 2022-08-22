import socket            
from pynput.mouse import Listener, Controller
import re
import time


class mouseAndKeyboardConnection():
  def __init__(self)-> None:
    self.initSocket()


  def initSocket(self)-> None:
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
    print ("Socket successfully created")


  def listenForConnections(self, port : int):
    self.s.bind(('', port))        
    self.s.listen(5)    
    print ("socket is listening")


  def acceptConnections(self)-> None:
    self.c, addr = self.s.accept()
    print ('Got connection from', addr )


  def sendMouseMovement(self)->None:
    self.listener =  Listener(on_move = self.on_move, on_click = self.on_click, on_scroll = self.on_scroll)
    self.listener.start()

  def connectToServer(self, serverIP : str, port : int)-> None:         
    self.s.connect((serverIP, port))#'192.168.0.6'


  def getMouseMovement(self)->int:
    mouse = Controller()
    while (True):
        data = self.s.recv(1024).decode()
        print(data)

        if (data == 'TERMINATE'):
            self.s.shutdown(socket.SHUT_RDWR)
            self.s.close()
            return(0)

        if (data != ''):
            try:
                x = re.search('aa(.*?)bb',data).group(1)
                y = re.search('bb(.*?)cc',data).group(1)
            except AttributeError:#invaild data will casuse AttributeError
                print("AttributeError")     
                continue
        else:
            continue

        x = int(x)
        y = int(y)
        mouse.position = (x, y)



  def on_move(self, x, y):
    self.c.send('aa{}bb{}cc'.format(x, y).encode())

  def on_click(self, x, y, button, pressed):
      print('{} {}'.format(button, 'Pressed' if pressed else 'Released'))


  def on_scroll(self, x, y, dx, dy):
      print('({}, {})'.format(dx, dy))

  def terminateSocket(self):
    try:
      for _ in range(0, 10):
        self.c.send('TERMINATE'.encode())
        self.c.send(' '.encode())
        print("sent")
        time.sleep(1)
    except:
      pass

    self.c.shutdown(socket.SHUT_RDWR)
    self.c.close()

    self.listener.stop()



# server = mouseAndKeyboardConnection()
# server.listenForConnections(12345)
# server.acceptConnections()
# server.sendMouseMovement()


# time.sleep(15)
# server.terminateSocket()

# print("Closed OK")

# from screeninfo import get_monitors

#Client

# for m in get_monitors():
#     print(str(m))

# print("S")