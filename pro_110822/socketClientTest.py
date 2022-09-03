import socket


def client_program():
    port = 12345 

    client_socket = socket.socket()  
    client_socket.connect(('192.168.0.5', port))  

    message = input(" -> ") 

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode()) 
        data = client_socket.recv(1024).decode() 
        print('Received from server: ' + data)  

        message = input(" -> ")  

    client_socket.close() 

if __name__ == '__main__':
    client_program()