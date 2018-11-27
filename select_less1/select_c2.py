# coding: utf-8
# __author__: ""


import socket

'''
示例2：IO多路复用--使用socket模拟多线程，并实现读写分离

'''
obj = socket.socket()
obj.connect(('127.0.0.1', 8003))

while True:
    inp = input('>>>')
    obj.sendall(bytes(inp, encoding='utf-8'))
    ret = str(obj.recv(1024),encoding='utf-8')
    print(ret)

obj.close()
