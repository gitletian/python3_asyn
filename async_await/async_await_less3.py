# coding: utf-8
# __author__: ""

import time
import asyncio


'''
使用async可以定义协程对象，使用await可以针对耗时的操作进行挂起，就像生成器里的yield一样，函数让出控制权。
协程遇到await，事件循环将会挂起该协程，执行别的协程，直到其他的协程也挂起或者执行完毕，再进行下一个协程的执行
耗时的操作一般是一些IO操作，例如网络请求，文件读取等。我们使用asyncio.sleep函数来模拟IO操作。协程的目的也是让这些IO操作异步化。
'''


def callback(future):
    print("callback:", future.result())

#
# now = lambda: time.time()
#
# async def do_some_work(x):
#     print("waiting:", x)
#     # await 后面就是调用耗时的操作
#     await asyncio.sleep(x)
#     return "Done after {}s".format(x)
#
#
# start = now()
#
# coroutine = do_some_work(2)
# loop = asyncio.get_event_loop()
# task = asyncio.ensure_future(coroutine)
# task.add_done_callback(callback)
# loop.run_until_complete(task)
#
# print("Task ret:", task.result())
# print("Time:", now() - start)
#


now = lambda: time.time()

async def do_some_work(x):
    print("waiting:", x)
    # await 后面就是调用耗时的操作
    await asyncio.sleep(x)
    return "Done after {}s".format(x)


async def do_some_work2(x):
    print("waiting:", x)
    # await 后面就是调用耗时的操作
    '''
    在await asyncio.sleep(x)，因为这里sleep了，模拟了阻塞或者耗时操作，这个时候就会让出控制权。
    即当遇到阻塞调用的函数的时候，使用await方法将协程的控制权让出,以便loop调用其他的协程。
    '''
    await asyncio.sleep(x)
    return "Done after 22  {}s".format(x)


start = now()

loop = asyncio.get_event_loop()

coroutine1 = do_some_work(4)
coroutine2 = do_some_work2(2)
'''
公用了同一个 loop, 所以 不用 wait 不用添加 也 task2 也已经 在 loop的task里面了
'''
task1 = asyncio.ensure_future(coroutine1)
task1.add_done_callback(callback)

task2 = asyncio.ensure_future(coroutine2)
task2.add_done_callback(callback)


# loop.run_until_complete(task1)
loop.run_until_complete(asyncio.wait([task1, task2]))

# print("Task ret:", task.result())
print("Time:", now() - start)

