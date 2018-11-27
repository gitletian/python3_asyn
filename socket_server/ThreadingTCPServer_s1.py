# coding: utf-8
# __author__: ""
'''
SocketServer实现服务器
'''

import socketserver


class MyServer(socketserver.BaseRequestHandler):

    def handle(self):
        # print self.request,self.client_address,self.server
        conn = self.request
        conn.sendall('欢迎致电 10086，请输入1xxx,0转人工服务.'.encode("utf-8"))
        Flag = True
        while Flag:
            data = conn.recv(1024).decode("utf-8")
            print(data)
            print(type(data))
            if data == 'exit':
                Flag = False
            elif data == '0':
                conn.sendall(bytes('通过可能会被录音.balabala一大推', "utf-8"))
            else:
                conn.sendall('请重新输入.'.encode("utf-8"))


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 8011), MyServer)
    server.serve_forever()

