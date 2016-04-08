import socket
import sys

s = socket.socket()
s.connect(("localhost",9999))
f=open ("demo.txt", "rb") 

l = f.read(1024)
print l
while (l):
    s.send(l)
    l = f.read(1024)
s.close()

