import socket
import sys
from collections import namedtuple
import pickle
import threading
import inspect
import time
import signal
import errno

port = 7735
receiver = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
receiver.bind(('', port) )
host = ''

receiver.listen(10) # Acepta hasta 10 conexiones entrantes.


def rdt_recv(filename):
    while True:
        sc, address = receiver.accept()

        #print address

        f = open(filename,'wb') #open in binary
        #i=i+1
        #pSimple_UDP_receiverrint(i)
        l = 1
        while(l):
            l = sc.recv(1024)
            while (l):
                f.write(l)
                l = sc.recv(1024)
            f.close()


        sc.close()

receiver.close()
