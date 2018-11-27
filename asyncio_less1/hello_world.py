# coding: utf-8
# __author__: ""

import asyncio
import threading

@asyncio.coroutine
def hello():
    print("hello world1 thringid = {0}".format(threading.current_thread()))

    # 异步调用 asyncio.sleep(1)
    r = yield from asyncio.sleep(3)
    print("hello again 1 thringid = {0}".format(threading.current_thread()))


@asyncio.coroutine
def hello2():
    print("hello2 world2 thringid = {0}".format(threading.current_thread()))

    # 异步调用 asyncio.sleep(1)
    r = yield from asyncio.sleep(1)
    print("hello2 again 2 thringid = {0}".format(threading.current_thread()))



# 获取 eventloop
loop = asyncio.get_event_loop()
# 执行 coroutine (协程)
import time
t = int(time.time())
loop.run_until_complete(asyncio.wait([hello(), hello2()]))
print(int(time.time() - t))

loop.close()

