# server2.py
import socket
from threading import Thread
from SocketServer import ThreadingMixIn
import platform

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024
version = 'P2P-CI/2.0'

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print " New thread started for "+ip+":"+str(port)

    def run(self):
        ReqMsg = self.sock.recv(1024)
        print '\nGot a request message:'
        print '\n--------------------------------'
        print ReqMsg
        print '--------------------------------'
        mindex = ReqMsg.find(' ')# method index
        method =  ReqMsg[0:mindex]
        rindex = ReqMsg.find('RFC')#RFC index
        vindex = ReqMsg.find('P2P-CI/')#version index
        peerversion = ReqMsg[vindex:vindex+10]
        RFCno =  ReqMsg[rindex+4:vindex-1]


        if (RFCno != 'ALL'):
            RFCno =  int(RFCno)
        if method == 'GET':
            status = '200 OK'
        else:
            status = '400 Bad Request'
        if peerversion!=version:
            status = '505 P2P-CI Version Not Supported'
        Rindex = ReqMsg.find('RFC ')
        RFCno = ReqMsg[Rindex+4:vindex-1]
        filename = 'rfc'+RFCno+'.txt'
        try:
            f = open(filename,'r+')
        except IOError:
            status = '404 Not Found'
        ResMsg = version+' '+status+'\n'+'OS: '+ platform.system()+platform.release()
        self.sock.send(ResMsg)

        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sock.send(l)
                #print('Sent ',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                self.sock.close()
                break

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    print "Waiting for incoming connections..."
    (conn, (ip,port)) = tcpsock.accept()
    print 'Got connection from ', (ip,port)
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
