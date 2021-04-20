#tutorial from https://dev.to/zeyu2001/build-a-chatroom-app-with-python-44fa
#information on threading @ Real Python https://realpython.com/intro-to-python-threading/#what-is-a-thread

import threading 
import socket 
import argparse
import os

class Server(threading.Thread):
    #server class inherits from Python threading.Thread class - initializing a thread. 
    #when start() is called on a server object then run() will be completed in parallel to existing thread 
    #what is threading?! Threading allows you to run two or more different parts of program simultaneously (or appear to in python 3)-"multithreading"
    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.host = host
        self.port = port

    def run(self):
        #Sockets --- An IP address(HOST) and a port number(identifies the application that should recieve data) pair 
        #(perhaps similar to devices used at TDA - connecting IPs of smart devices to home network ports)
        # Source (IP: Port Num) --> Destination (IP: Port Num)

        #create socket object: takes two args: address family (AF_NET) for IP NETWORKING and socket type (SOCK_STREAM) for reliable flow-controlled data streams (TCP)- OR(UDP = SOCK_DGRAM)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #SO_REUSEADDR allows server to  use same port after an old connection closes 
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #binds the socket object to a socket address on the server bind (IP Address(str), Port Number(int)) takes in tuples 
        sock.bind(self.host, self.port)

        #TCP uses two kinds of sockets: listening and connected 
        #after calling listen() on socket  it can only establish coneection of 'handshakes' but not data transfer (need new socket for client connection)
        sock.listen(1)
        print('Listening at', sock.getsockname())

        #loopback interface = IP address 127.0.0.1 (JUST LIKE TDA) localhost 
        #We can specifiy any IP interface with the bind() function . Ex. localhost OR '' for packets arrivign at the server from any network interfaces

        #infinite loop to listen for new client side connections 
        while True:

            #accept new connection- return a new connected socket and socket address of client
            sc, sockname = sock.accept()

            #getpeername() returns socket address on other end of connection (client) while getsockname() returns socket address to which socket object is bound
            print('Accepted a new connection from {} to {}'.format(sc.getpeername(), sc.getsockname()))
            # print(f'Accepted a new Connection from {} to {}') how to format this in an f string with sc.getpeername etc.? 

            #create a new thread 
            #must communicate with each client WHILE also listening for other connections/clients 
            #evertime a new client connects a new ServerSocket thread runs alongsided Server thread
            server_socket = ServerSocket(sc, sockname, self)

            #start new thread 
            server_socket.start()

            #Add thread to active connections 
            #way for server to manage all the active client connections - stores in self.connections
            self.connections.append(server_socket)
            print('Ready to receive messages from', sc.getpeername())