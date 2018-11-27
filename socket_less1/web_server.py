# coding: utf-8
# __author__: ""

import socket
import time


j = 0


def handle_request(client):
    global j
    j += 1
    print("============process======{0}".format(j))
    # buf = client.recv(1024)
    client.send("HTTP/1.1 200 OK\r\n\r\n".encode('utf-8'))
    client.send("Hello, World".encode('utf-8'))


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8088))
    sock.listen(5)
    i = 0
    while True:
        i += 1
        print("=================={0}".format(i))
        connection, address = sock.accept()
        time.sleep(5)
        handle_request(connection)
        connection.close()


if __name__ == '__main__':
    main()




'''
# UDP

import socket
ip_port = ('127.0.0.1',9999)
sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
sk.bind(ip_port)

while True:
    data = sk.recv(1024)
    print data




import socket
ip_port = ('127.0.0.1',9999)

sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
while True:
    inp = raw_input('数据：').strip()
    if inp == 'exit':
        break
    sk.sendto(inp,ip_port)

sk.close()


'''

