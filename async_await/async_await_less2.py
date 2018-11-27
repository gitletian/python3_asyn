# coding: utf-8
# __author__: ""

import time
import asyncio


def callback(future):
    print("callback:", future.result())


now = lambda: time.time()

async def do_some_work(x):
    print("waiting:", x)
    return 'aaaa'


start = now()
# 这里是一个协程对象，这个时候do_some_work函数并没有执行
coroutine = do_some_work(2)
print(coroutine)

#  创建一个事件loop
loop = asyncio.get_event_loop()
'''
协程对象不能直接运行，在注册事件循环的时候，其实是run_until_complete方法将协程包装成为了一个任务（task）对象.
task对象是Future类的子类，保存了协程运行后的状态，用于未来获取协程的结果
'''
# task = loop.create_task(coroutine)
task = asyncio.ensure_future(coroutine)

print(task)
task.add_done_callback(callback)
print(task)
# 将协程加入到事件循环loop
loop.run_until_complete(task)

print(task)

print("Time:", now() - start)

