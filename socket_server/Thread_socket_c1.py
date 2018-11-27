# coding: utf-8
# __author__: ""

'''
Thread_socket_client
'''

import socket
ip_port = ('0.0.0.0', 9999)
#买手机
s = socket.socket()
#拨号
s.connect(ip_port)
#发送消息
welcome_msg = s.recv(1024)
print("from server:", welcome_msg.decode())
while True:
    send_data = input(">>: ").strip()
    if len(send_data) == 0:
        continue
    s.send(bytes(send_data, encoding='utf8'))

    # 收消息
    recv_data = s.recv(1024)
    print(str(recv_data, encoding='utf8'))
    # 挂电话
s.close()

