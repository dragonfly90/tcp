import socket
import sys
from collections import namedtuple
import pickle
import threading
import inspect
import time
import signal
import errno

#sender = socket.socket(socket.AF_INFT, socket.SOCK_DGRM)
#sender_port = 62223
#sender.bind(('',sender_port))

#s.connect(("localhost",9999))

#def rdt_send(filename, rcv_host):
#    f=open (filename, "rb")
#    l = f.read(1024)

#    while (l):
#        s.send(l)
#        l = f.read(1024)
        
#s.close()

def rdt_send(filename,rcv_host):
    sender = socket.socket()
    sender.connect(("localhost",9999))
    f=open (filename, "rb")

    l = f.read(1024)
    print l
    while (l):
        sender.send(l)
        l = f.read(1024)
    sender.close()