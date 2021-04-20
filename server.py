#tutorial from https://dev.to/zeyu2001/build-a-chatroom-app-with-python-44fa
#information on threading @ Real Python https://realpython.com/intro-to-python-threading/#what-is-a-thread

import threading 
import socket 
import argparse
import os

class Server(threading.Thread):
    #server class inherits from Python threading.Thread class - initializing a thread. 
    #when start() is called on a server object then run() will be completed in parallel to existing thread 
    # what is threading?! Threading allows you to run two or more different parts of program simultaneously (or appear to in python 3)-
    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.host = host
        self.port = port

    def run(self):
        pass