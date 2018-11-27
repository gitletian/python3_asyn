# coding: utf-8
# __author__: ""

import socket
ip_port = ('127.0.0.1',9999)
sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
sk.bind(ip_port)

while True:
    data = sk.recv(1024)
    print(data)



'''
UDP
'''
'''

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