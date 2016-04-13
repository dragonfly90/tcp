import socket
import time
import platform
import os
import pickle
import random
from thread import *
from threading import Thread
import threading
import sys

from SocketServer import ThreadingMixIn
import ThreadTCP
import SocketServer

version = 'P2P-CI/2.0'
rcv_rfc_num = ''  #record rfc_num for rdt_recv()
rcv_rfc_title = ''
threads = []


def PeerFormRequestMessage(method,RFCno,self_host,upload_port):
    message = method + ' '+'RFC '+str(RFCno) +' '+ version + '\n' + 'Host: '+ self_host + '\n'+ 'OS: '+ platform.system()+platform.release()
    return message


def p2p_get_request(rfc_num, peer_host, peer_upload_port):
    global upload_socket
    global rcv_rfc_num
    rcv_rfc_num = rfc_num
    data = p2p_request_message(rfc_num, host)
    data = pickle.dumps(data)



    portnumber=int(peer_upload_port)
    print portnumber
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((peer_host, portnumber))
    print portnumber

    method = 'GET'
    RFCno = rfc_num


    ReqMsg = PeerFormRequestMessage(method,RFCno,peer_host,portnumber)
    client.send(ReqMsg)

    ResMsg = client.recv(128)
    print  '\n'+ResMsg
    rfc_path = os.getcwd() + "/rfc"
    filename = '/rfc'+RFCno+'.txt'

    with open(rfc_path+filename, 'wb') as f:
        print 'file opened'
        while True:
        #print('receiving data...')
            data = client.recv(BUFFER_SIZE)
            print('data=%s', (data))
            if not data:
                f.close()
                print 'file close()'
                break
            # write data to a file
            f.write(data)

    print('Successfully get the file')
    client.close()
    print('connection closed')
    #upload_socket.sendto(data,(peer_host, int(peer_upload_port)))

# display p2p response message
def p2p_response_message(filename): # the parameter "rfc_num" should be str
    current_time = time.strftime("%a, %d %b %Y %X %Z", time.localtime())
    OS = platform.system()
    if os.path.exists(filename) == False:
        status = "404"
        phrase = "Not Found"
        message = "P2P-CI/1.0 "+ status + " "+ phrase + "\n"\
                    "Date:" + current_time + "\n"\
                    "OS: "+str(OS)+"\n"
    else:
        status = "200"
        phrase = "OK"
        last_modified = time.ctime(os.path.getmtime(filename))
        content_length = os.path.getsize(filename)
        message = ["P2P-CI/1.0 "+ status + " "+ phrase + "\n"\
                  "Date: " + current_time + "\n"\
                  "OS: " + str(OS)+"\n"\
                  "Last-Modified: " + last_modified + "\n"\
                  "Content-Length: " + str(content_length) + "\n"\
                  "Content-Type: text/text \n"]
                  #+ str(data)

    return message, filename

# display p2p request message
def p2p_request_message(rfc_num, host):
    OS = platform.platform()
    message = "GET RFC "+str(rfc_num)+" P2P-CI/1.0 \n"\
              "Host: "+str(host)+"\n"\
              "OS: "+str(OS)+"\n"
    return message


# display p2s request message for ADD method
def p2s_add_message(rfc_num, host, port, title):  # for ADD
    message = "ADD" + " RFC " + str(rfc_num)+" P2P-CI/1.0 \n"\
              "Host: " + str(host)+"\n"\
              "Port: " + str(port)+"\n"\
              "Title: " + str(title)+"\n"
    return [message, rfc_num, host, port, title]


# display p2s request message for LOOKUP method
def p2s_lookup_message(rfc_num, host, port, title, get_or_lookup):  # LOOKUP method
    message = "LOOKUP" + " RFC " + str(rfc_num)+" P2P-CI/1.0 \n"\
              "Host: " + str(host)+"\n"\
              "Port: " + str(port)+"\n"\
              "Title: " + str(title)+"\n"
    return [message, rfc_num, get_or_lookup]


#display p2s request message for LIST methods
def p2s_list_request(host, port):
    message = "LIST ALL P2P-CI/1.0 \n"\
              "Host: "+str(host)+"\n"\
              "Port: "+str(port)+"\n"
    return message


#get the list of the local rfcs
def get_local_rfcs():
    rfcs_path = os.getcwd() + "/rfc"
    rfcs_num = [num[num.find("c")+1:num.find(".")] for num in os.listdir(rfcs_path) if 'rfc' in num]
    return rfcs_num

def get_local_rfcs_title():
    rfcs_path = os.getcwd() + "/rfc"
    rfcs_title = [title[0:title.find(".")] for title in os.listdir(rfcs_path) if 'rfc' in title]
    return rfcs_title

#pass peer's hostname, port number and rfc_num, rfc_title
def peer_information():
    keys = ["RFC Number", "RFC Title"]
    rfcs_num = get_local_rfcs()
    rfcs_title = get_local_rfcs_title()
    for num, title in zip(rfcs_num, rfcs_title):
        entry = [num, title]
        dict_list_of_rfcs.insert(0, dict(zip(keys, entry)))
    return [upload_port_num, dict_list_of_rfcs]  # [port, rfcs_num, rfcs_title]



def print_combined_list(dictionary_list, keys):
    for item in dictionary_list:
        print(' '.join([item[key] for key in keys]))

#get the input from user
def get_user_input(strr, i):
    user_input = raw_input("> Enter ADD, LIST, LOOKUP, GET, or EXIT:  \n")

    if user_input == "EXIT":
        data = pickle.dumps("EXIT")
        s.send(data)
        s.close                     # Close the socket when done
        os._exit(1)
    elif user_input == "ADD":
        user_input_rfc_number = raw_input("> Enter the RFC Number: ")
        user_input_rfc_title = raw_input("> Enter the RFC Title: ")
        data = pickle.dumps(p2s_add_message(user_input_rfc_number, host, upload_port_num, user_input_rfc_title))
        s.send(data)
        server_data = s.recv(1024)
        #print(server_data.decode('utf-8'))
        get_user_input("hello", 1)
    elif user_input == "LIST":
        data = pickle.dumps(p2s_list_request(host, port))

        s.send(data)
        server_data = s.recv(1024)


        new_data = pickle.loads(s.recv(1000000))
        print_combined_list(new_data[0], new_data[1])

        get_user_input("hello", 1)
    elif user_input == "GET":
        user_input_rfc_number = raw_input("> Enter the RFC Number: ")
        user_input_rfc_title = raw_input("> Enter the RFC Title: ")
        global rcv_rfc_title
        rcv_rfc_title = str(user_input_rfc_title)
        data = pickle.dumps(p2s_lookup_message(user_input_rfc_number, host, port, user_input_rfc_title, "0"))
        s.send(data)
        server_data = pickle.loads(s.recv(1024))
        if not server_data[0]:
            print(server_data[1])
            get_user_input("hello", 1)
        else:
            print server_data[0]["Hostname"], server_data[0]["Port Number"]
            p2p_get_request(str(user_input_rfc_number), server_data[0]["Hostname"], server_data[0]["Port Number"])
        get_user_input("hello", 1)
    elif user_input == "LOOKUP":
        user_input_rfc_number = raw_input("> Enter the RFC Number: ")
        user_input_rfc_title = raw_input("> Enter the RFC Title: ")
        data = pickle.dumps(p2s_lookup_message(user_input_rfc_number, host, port, user_input_rfc_title, "1"))
        #print(p2s_lookup_message(user_input_rfc_number, host, port, user_input_rfc_title))
        #print(data)
        s.send(data)
        server_data = pickle.loads(s.recv(1024))
        #print(server_data[0][3])
        #print(server_data[0][1])
        print(server_data[1])
        keys = ['RFC Number', 'RFC Title', 'Hostname', 'Port Number']
        print_combined_list(server_data[0], keys)
        get_user_input("hello", 1)
    else:
        get_user_input("hello", 1)

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



class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):

        print "Waiting for incoming connections..."
        #(conn, (ip,port)) = self.accept()
        print 'Got connection from ', self.client_address

        ReqMsg = self.request.recv(1024)
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

        rfc_path = os.getcwd() + "/rfc"

        filename = '/rfc'+RFCno+'.txt'
        try:
            f = open(rfc_path+filename,'r+')
        except IOError:
            status = '404 Not Found'
        ResMsg = version+' '+status+'\n'+'OS: '+ platform.system()+platform.release()
        self.request.send(ResMsg)

        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.request.send(l)
                #print('Sent ',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                self.request.close()
                break

TCP_IP = socket.gethostname()
BUFFER_SIZE = 1024
upload_port_num = 9001  # generate a upload port randomly in 65000~65500
TCP_PORT = upload_port_num


dict_list_of_rfcs = []  # list of dictionaries of RFC numbers and Titles.

s=socket.socket()          # Create a socket object

host = socket.gethostname()  # Get local machine name

port = 7734                  # Reserve a port for your service.
s.connect((host, port))
data = pickle.dumps(peer_information())  # send all the peer information to server
s.send(data)

data = s.recv(1024)
print(data.decode('utf-8'))
s.close

start_new_thread(get_user_input, ("hello", 1))


if __name__ == "__main__":

    host = TCP_IP                       # Get local machine name
    port = TCP_PORT                  # Reserve a port for your service.




    server_A = ThreadTCP.ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)


    server_A_thread = threading.Thread(target=server_A.serve_forever)


    server_A_thread.setDaemon(True)


    server_A_thread.start()


    while 1:
        time.sleep(1)


    for t in threads:
        t.join()






