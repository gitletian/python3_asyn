# coding: utf-8
# __author__: ""
'''
Thread_socket_server
'''

import socketserver
import subprocess


class MyServer(socketserver.BaseRequestHandler):
    def handle(self):

        self.request.sendall(bytes('欢迎致电10086，请输入1xx,0转入人工服务', encoding='utf-8'))
        while True:
            data = self.request.recv(1024)
            print('------>%s' % (len(data)))
            if len(data) == 0:
                break
            print("[%s] says:%s" %(self.client_address, data.decode()))
            # self.request.sendall(data.upper())
            cmd = subprocess.Popen(data.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            cmd_res = cmd.stdout.read()
            if not cmd_res:
                cmd_res = cmd.stderr.read()
            if len(cmd_res) == 0:  # cmd has no output
                cmd_res = bytes('cmd has output', encoding='utf-8')
            # self.request.sendall(data.upper())
            self.request.send(cmd_res)


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('0.0.0.0', 9999), MyServer)
    server.serve_forever()

