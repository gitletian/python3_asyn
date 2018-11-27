# coding: utf-8
# __author__: ""


import asyncio
import time
from threading import Thread

now = lambda: time.time()


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

async def do_some_work(x):
    print('Waiting {}'.format(x))
    await asyncio.sleep(x)  # 异步 协程
    print('Done after {}s'.format(x))


def more_work(x):
    print('More work {}'.format(x))
    time.sleep(x)  # 同步阻塞
    print('Finished more work {}'.format(x))

start = now()
new_loop = asyncio.new_event_loop()
t = Thread(target=start_loop, args=(new_loop,))
t.start()
print('TIME: {}'.format(time.time() - start))

'''
很多时候，我们的事件循环用于注册协程，而有的协程需要动态的添加到事件循环中。
一个简单的方式就是使用多线程。当前线程创建一个事件循环，然后在新建一个线程，在新线程中启动事件循环。当前线程不会被block。
启动上述代码之后，当前线程不会被block，新线程中会按照顺序执行call_soon_threadsafe方法注册的more_work方法，
后者因为time.sleep操作是同步阻塞的，因此运行完毕more_work需要大致6 + 3

'''
new_loop.call_soon_threadsafe(more_work, 6)
new_loop.call_soon_threadsafe(more_work, 5)

'''
上述的例子，主线程中创建一个new_loop，然后在另外的子线程中开启一个无限事件循环。
 主线程通过run_coroutine_threadsafe新注册协程对象。
 这样就能在子线程中进行事件循环的并发操作，同时主线程又不会被block。一共执行的时间大概在6s左右。
'''

# asyncio.run_coroutine_threadsafe(do_some_work(6), new_loop)
# asyncio.run_coroutine_threadsafe(do_some_work(4), new_loop)

