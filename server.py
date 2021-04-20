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
        sock.bind((self.host, self.port))

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

    def broadcast(self, message, source):
        #How it works: 1. client sends message -> server (GUI or commandline) 2. Server recieves and processes message
        #3. server sends message to all connected clients 4. clients will display mesage in command line or GUI 
        #broadcast is a misnomer --- really sending many 'unicasts' one to one transission to each connected client. 

        #self.connections is a list of ServerSocket objects (active client connections)
        for connection in self.connections:

            #send to all connected clients except source 
            if connection.sockname != source:
                connection.send(message)

class ServerSocket(threading.Thread):
    #class facilitates communication with indv. clients 

    def __init__(self, sc, socketname, server):
        super().__init__()
        self.sc = sc
        self.sockname = socketname
        self.server = server

    def run(self):

        #infinite loop - listening for data sent by the client
        while True:
            message = self.sc.recv(1024).decode('ascii')
            if message:
                print(f'{self.sockname} says {message}')
                self.server.broadcast(message, self.sockname)
            else:
                #client closed the socket - exit thread
                print(f'{self.socketname} has closed the connection')
                self.sc.close()
                server.remove_connection(self)
                return 

    def send(self, message):
        self.sc.sendall(message.encode('ascii'))

    def exit(server):
        #when a client socket is closed it returns an empty string - removed the ServerSocket thread from the list of active connections/end thread
        while True:
            ipt = input('')
            if ipt == 'q':
                print('Closing all connections...')
                for connection in server.connections:
                    connection.sc.close()
                print('Shutting down the server...')
                os._exit(0)

    # if __name__ == '__main__':
    #     parser = argparse.ArgumentParser(description='Chatroom Server')
    #     parser.add_argument('host', help='Interface the server listens at')
    #     parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port (default 1060)')
    #     args = parser.parse_args()

    #     #create and start server thread
    #     server = Server(args.host, args.p)
    #     server.start()

    #     exit = threading.Thread(target = exit, args = (server,))
    #     exit.start()