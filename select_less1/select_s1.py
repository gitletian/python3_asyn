# coding: utf-8
# __author__: ""

import socket
import select

sk1 = socket.socket()
sk1.bind(('0.0.0.0', 8001))
sk1.listen()

sk2 = socket.socket()
sk2.bind(('0.0.0.0', 8002))
sk2.listen()

sk3 = socket.socket()
sk3.bind(('0.0.0.0', 8003))
sk3.listen()

inputs = [sk1, sk2, sk3, ]

while True:
    r_list, w_list, e_list = select.select(inputs,[],inputs,3)
    print("111=====")
    for sk in r_list:
        # conn表示每一个连接对象
        print("22====={0}".format(sk))
        conn, address = sk.accept()
        print("33====={0}===={1}".format(conn, address))
        conn.sendall(bytes('hello', encoding='utf-8'))
        conn.close()

    for sk in e_list:
        inputs.remove(sk)

'''
解释：
    # select内部自动监听sk1,sk2,sk3三个对象，监听三个句柄是否发生变化，把发生变化的元素放入r_list中。
    # 如果有人连接sk1，则r_list = [sk1]
    # 如果有人连接sk1和sk2，则r_list = [sk1,sk2]
    # select中第1个参数表示inputs中发生变化的句柄放入r_list。
    # select中第2个参数表示[]中的值原封不动的传递给w_list。
    # select中第3个参数表示inputs中发生错误的句柄放入e_list。
    # 参数1表示1秒监听一次
     # 当有用户连接时，r_list里面的内容[<socket.socket fd=220, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 8001)>]

服务端s1.py
'''
