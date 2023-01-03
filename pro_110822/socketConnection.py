import socket            
from pynput.mouse import Listener, Controller


import sys
import traceback
import logging
import re

import pdb


class MouseAndKeyboardConnection():
  def __init__(self)-> None:#None : blocking, 0 : None
    pass


  def create_socket(self, socketTimeout: int)-> None:
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


  def listen_for_connections(self, port : int):
    try:
      if (self.is_port_in_use(12345)):
        print ("port is not availabel")
      else:
        self.s.bind(('', port))        
        self.s.listen()    
        print ("port availabel socket is listening")
    except:
      part1 = str(sys.exc_info())
      part2 = traceback.format_exc()
      origin = re.search(r'File(.*?)\,', part2).group(1) 
      loggMessage = origin + '\n' + part1  + '\n' + part2
      logging.info(loggMessage)

  def accept_connections(self)-> None:
    self.c, addr = self.s.accept()
    return self.c, addr 


  def accept_client_connection(self, clientIP):
    self.c, addr = self.s.accept()
    while(addr[0] != clientIP):
      self.c.shutdown(socket.SHUT_RDWR)
      self.c.close()
      self.c, addr = self.s.accept()


  def send_mouse_movement(self)->bool:
    self.listener =  Listener(on_move = self.on_move, on_click = self.on_click, on_scroll = self.on_scroll)
    self.listener.start()

  def connect_to_server(self, serverIP : str, port : int)-> None:
    try:
      self.s.connect((serverIP, port))
    except:
      print ("Connection refuesd at {}:{}".format(serverIP, port))
      part1 = str(sys.exc_info())
      part2 = traceback.format_exc()
      origin = re.search(r'File(.*?)\,', part2).group(1) 
      loggMessage = origin + '\n' + part1  + '\n' + part2 + "\nserverIP: " + serverIP + "\nport: " + str(port)
      logging.info(loggMessage)
      return False
    return True


  def recive_mouse_movement(self)->int:
    mouse = Controller()
    print("Reciving mouse movement")
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
        print("x:", x, "y:", y)
        mouse.position = (x, y)



  def on_move(self, x, y):
    self.c.send('aa{}bb{}cc'.format(x, y).encode())

  def on_click(self, x, y, button, pressed):
      print('{} {}'.format(button, 'Pressed' if pressed else 'Released'))


  def on_scroll(self, x, y, dx, dy):
      print('({}, {})'.format(dx, dy))





  def terminate_socket(self):
    try:
      if(self.still_connected()):
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
    



  def still_connected(self)-> bool:
    try:
      self.c.sendall(b"bing")
      return True
    except:
      return False

  def is_port_in_use(self, port: int)-> bool:
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
