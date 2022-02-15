#!/usr/bin/python3

from socket import *

# Server info
server_port = 12002
server_address = "192.168.0.16"

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((server_address, server_port))
# Maximum connections allowed
server_socket.listen(1)

print("[ LISTENING ON PORT ] " + str(server_port))

while True:
    client_socket, client_address = server_socket.accept()
    
    try:
    	# Prints client ip and receives request
        print("[ CONNECTION FROM ] " + str(client_address))
        message = client_socket.recv(1024) 
        print(message)
    
    	# Opens the correspending HTML file and returns it with a status code
        filename = message.split()[1]
        f = open(filename[1:])
        # Logs the client request
        log_file = open('logfile.txt', 'w')
        outputdata = f.read()
        log_file.write(str(message))
        log_file.close()    
        f.close()
        client_socket.send(bytes(str.encode("HTTP/1.1 200 OK\r\n\r\n")))
        for i in range(0, len(outputdata)):
            client_socket.send(bytes(outputdata[i].encode()))
        
    except FileNotFoundError:
        client_socket.send(bytes(str.encode("HTTP/1.1 404 Not Found\r\n\r\n")))
        client_socket.send(bytes(str.encode("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")))

    except Exception as err:
        client_socket.send(bytes(str.encode("HTTP/1.1 400 Bad Request\r\n\r\n")))
        client_socket.send(bytes(str.encode("<html><head></head><body><h1>400 Bad Request</h1></body></html>\r\n")))
        print(err)
    client_socket.close()

server_socket.close()
