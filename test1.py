# coding: utf-8
# __author__: ""

import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer
from tornado.netutil import bind_sockets
from tornado.process import fork_processes


class MainHandler(tornado.web.RequestHandler):
    def post(self):
        self.write("Hello, world")

# Tornado Web框架的核心应用类，是与服务器对接的接口，里面保存了路由信息表
app = tornado.web.Application([
    (r"/index", MainHandler),
    (r"/", MainHandler),
],
    # debug=True
)

if __name__ == "__main__":
    # 创建服务器实例, 并绑定到给定的端口上
    # server = app.listen(8888) # 这种方式不支持多进程

    # 第一种多进程
    server = HTTPServer(app)
    server.bind(8888)
    server.start(1)  # 启动多进程

    # 第二种多进程
    # sockets = bind_sockets(8888)
    # fork_processes(2)
    # server = HTTPServer(app)
    # server.add_sockets(sockets)

    # tornado的核心io循环模块，封装了Linux的epoll和BSD的kqueue，tornado高性能的基石
    # 启动IOLoop实例的I/O循环,同时服务器监听被打开。
    tornado.ioloop.IOLoop.current().start()


