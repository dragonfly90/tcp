import socket
backlog = 1 #Number of queues

sk_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

local = {"port":1433}
internet = {"port":9999}

sk_1.bind (('', internet["port"]))
sk_1.listen(backlog)

sk_2.bind (('', local["port"]))
sk_2.listen(backlog)
