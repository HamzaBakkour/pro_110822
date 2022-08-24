from connection import mouseAndKeyboardConnection


x = mouseAndKeyboardConnection()
x.createSocket(2)
x.connectToServer('192.168.0.5', 12345)


print("S")