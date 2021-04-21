#Similar to the server.py we are using multithreading to send and recieve calls alongside one another (real-time chat isstead of alt. between send/recieve)
# the Send class thread is always listening for user input (from command line -> gui coming later)



import threading 
import socket
import argparse
import os
import sys


class Send(threading.Thread):
    #Send class inherits from Python threading.Thread class - initializing a thread. 
    #when calling start() on a Send/Receive object then run() will be completed in parallel to existing thread 
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name 

    def run(self):

        while True:
            message = input(f'{self.name}: ')

            #Type 'QUIT' to leave chat
            if message == 'QUIT':
                self.sock.sendall(f'Server: {self.name}'.encode() + f' has left the chat.')
                break

            #send message to server for broadcasting 
            else:
                self.sock.sendall(f'{self.name}: {message}'.encode())
        #I accidently put print in the else and it Quitting everytime I typed! ***PAY ATTENTION TO ALIGNMENT DETAILS!!
        print('\nQuitting...')
        self.sock.close()
        os._exit(0)

class Receive(threading.Thread):
  #Receive class inherits from Python threading.Thread class - initializing a thread. 
    #when calling start() on a Send/Receive object then run() will be completed in parallel to existing thread 
   
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name 

    def run(self):

        while True:
            message = self.sock.recv(1024)
            if message:
                # .decode()
                print(f'{message} \n {self.name}', end = '')
            else:
                #Server has closed the socket: exit program
                print('\n Uh oh - we have lost connection to the server!')
                print('\nQuitting...')
                self.sock.close()
                os._exit(0)

#connecting to the server: 

class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        print(f'Trying to connect to {self.host} : {self.port} ')
        # client calls .connect() method to connect a certain socket address (a tuple) of the server 
        #if the socket is not ready to receive connections (ex. server not running yet) then .connect() will FAIL
        self.sock.connect((self.host, self.port))
        print(f'Successfully connected to {self.host} : {self.port}')

        print()
        name = input('Your name: ')

        print()
        print(f'Welcome {name}! Getting ready to send and recieve messages...')

        #create send and receive threads
        send = Send(self.sock, name)
        receive = Receive(self.sock, name)

        #start send and receive threads
        send.start()
        receive.start()

        self.sock.sendall(f'Server: {name}  has joined the chat! Say hi '.encode() )
        print('\nAll set! Leave the chat anytime by typing "QUIT"\n')
        print(f'{name}', end = '')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chatroom Server')
    parser.add_argument('host', help='Interface the server listens at')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port (default 1060)')

    args = parser.parse_args()

client = Client(args.host, args.p)
client.start()