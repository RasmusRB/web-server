#!/usr/bin/python3

from socket import *

# Server info
server_port = 12001
server_address = "192.168.0.16"

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((server_address, server_port))

# Maximum connections allowed
server_socket.listen(1)

print("[ LISTENING ON PORT:",server_port,"] The server is ready to receive...")

while True:
    client_socket, client_address = server_socket.accept()
    
    try:
        print("[ CONNECTION FROM ]" + str(client_address))
        message = client_socket.recv(1024) 
        print(message)
    
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        f.close()
    
        client_socket.send(bytes(str.encode("HTTP/1.1 200 OK\r\n\r\n")))
        for i in range(0, len(outputdata)):
            client_socket.send(bytes(outputdata[i].encode()))
        
        client_socket.close()
    
    except IOError:
        client_socket.send(bytes(str.encode("HTTP/1.1 404 Not Found\r\n\r\n")))
        client_socket.send(bytes(str.encode("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")))
        client_socket.close()
        
    except IOError:
        client_socket.send(bytes(str.encode("HTTP/1.1 400 Bad Request\r\n\r\n")))
        client_socket.send(bytes(str.encode("<html><head></head><body><h1>400 Bad Request/h1></body></html>\r\n")))
        client_socket.close()
    
server_socket.close()


