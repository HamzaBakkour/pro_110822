import socket            
from pynput.mouse import Listener, Controller


import sys
import traceback
import logging
import re

import pdb


class mouseAndKeyboardConnection():
  def __init__(self)-> None:#None : blocking, 0 : None
    pass


  def createSocket(self, socketTimeout: int)-> None:
    try:
      self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
      self.s.settimeout(socketTimeout)
      self.c = socket.socket()
      print ("Socket successfully created")
    except:
      part1 = str(sys.exc_info())
      part2 = traceback.format_exc()
      origin = re.search(r'File(.*?)\,', part2).group(1) 
      loggMessage = origin + '\n' + part1  + '\n' + part2
      logging.info(loggMessage)


  def listenForConnections(self, port : int):
    try:
      if (self.isPortInUse(12345)):
        print ("port is not availabel")
      else:
        self.s.bind(('', port))        
        self.s.listen(5)    
        print ("port availabel socket is listening")
    except:
      part1 = str(sys.exc_info())
      part2 = traceback.format_exc()
      origin = re.search(r'File(.*?)\,', part2).group(1) 
      loggMessage = origin + '\n' + part1  + '\n' + part2
      logging.info(loggMessage)

  def acceptConnections(self)-> None:
    self.c, addr = self.s.accept()
    return self.c, addr 


  def acceptClientConnection(self, clientIP):
    self.c, addr = self.s.accept()
    while(addr[0] != clientIP):
      self.c.shutdown(socket.SHUT_RDWR)
      self.c.close()
      self.c, addr = self.s.accept()


  def sendMouseMovement(self)->bool:
    self.listener =  Listener(on_move = self.on_move, on_click = self.on_click, on_scroll = self.on_scroll)
    self.listener.start()

  def connectToServer(self, serverIP : str, port : int)-> None:
    try:
      self.s.connect((serverIP, port))#'192.168.0.6'
    except:
      # print ("Connection refuesd at {}:{}".format(serverIP, port))
      # part1 = str(sys.exc_info())
      # part2 = traceback.format_exc()
      # origin = re.search(r'File(.*?)\,', part2).group(1) 
      # loggMessage = origin + '\n' + part1  + '\n' + part2
      # logging.info(loggMessage)
      return False
    return True


  def reciveMouseMovement(self)->int:
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
                part1 = str(sys.exc_info())
                part2 = traceback.format_exc()
                origin = re.search(r'File(.*?)\,', part2).group(1) 
                loggMessage = origin + '\n' + part1  + '\n' + part2
                logging.info(loggMessage)
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
      if(self.stillConnected()):
        self.c.shutdown(socket.SHUT_RDWR)
        self.c.close()
        self.s.close()
        print("Connected Socket terminated")
    except :#trying to close c before any connections are acepted
                          # trying to close a connection that does not exist -> AttributeError
                          # occures when try to close the server before any connections are accepted
                          # part1 = str(sys.exc_info())
        part1 = str(sys.exc_info())
        part2 = traceback.format_exc()
        origin = re.search(r'File(.*?)\,', part2).group(1) 
        loggMessage = origin + '\n' + part1  + '\n' + part2
        logging.info(loggMessage)
      
    print("Not Connected Socket terminated")
    



  def stillConnected(self)-> bool:
    try:
      self.c.sendall(b"bing")
      return True
    except:
      return False

  def isPortInUse(self, port: int)-> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

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