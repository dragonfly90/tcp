# client2.py
#!/usr/bin/env python

import socket
import platform

version = 'P2P-CI/2.0'


def PeerFormRequestMessage(method,RFCno,self_host,upload_port):
    message = method + ' '+'RFC '+str(RFCno) +' '+ version + '\n' + 'Host: '+ self_host + '\n'+ 'OS: '+ platform.system()+platform.release()
    return message

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

method = 'GET'
RFCno = 1
peer_host = TCP_IP
peer_port = TCP_PORT

ReqMsg = PeerFormRequestMessage(method,RFCno,peer_host,peer_port)
s.send(ReqMsg)

ResMsg = s.recv(128)
print  '\n'+ResMsg

with open('received_file', 'wb') as f:
    print 'file opened'
    while True:
        #print('receiving data...')
        data = s.recv(BUFFER_SIZE)
        print('data=%s', (data))
        if not data:
            f.close()
            print 'file close()'
            break
        # write data to a file
        f.write(data)

print('Successfully get the file')
s.close()
print('connection closed')