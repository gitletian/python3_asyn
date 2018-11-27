# coding: utf-8
# __author__: ""

'''
客户端c1.py
示例1：模拟select，同时监听多个端口
'''
import socket

obj = socket.socket()
obj.connect(('127.0.0.1', 8001))

content = str(obj.recv(1024), encoding='utf-8')
print(content)

obj.close()

# # 客户端c2.py
# import socket
#
# obj = socket.socket()
# obj.connect(('127.0.0.1', 8002))
#
# content = str(obj.recv(1024), encoding='utf-8')
# print(content)
#
# obj.close()

