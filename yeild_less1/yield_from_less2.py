# coding: utf-8
# __author__: ""

# 例5 利用yield from语句向生成器（协程）传送数据
# 传统的生产者-消费者模型是一个线程写消息，一个线程取消息，通过锁机制控制队列和等待，但一不小心就可能死锁。
# 如果改用协程，生产者生产消息后，直接通过yield跳转到消费者开始执行，待消费者执行完毕后，换回生产者继续生产，效率极高：
'''
yield from 的主要功能是打开双向通道，把最外层的调用方与最内层的子生成器连接起来，
这样二者可以直接发送和产出值，还可以直接传入异常，而不用在位于中间的协程中添加大量处理异常的样板代码。
有了这个结构，协程可以通过以前不可能的方式委托职责。

子生成器：从 yield from 表达式中 <iterable> 部分获取的生成器；
委派生成器：包含 yield from <iterable> 表达式的生成器函数；
调用方：调用委派生成器的客户端代码；



1、接收 yield 的结果
2、代理， 双向通道
3、代替 for 迭代
4、异常处理

'''
import time


def consumer_work(len):
    # 读取send传进的数据，并模拟进行处理数据
    print("writer:")
    w = ''
    while True:
        print("===============wq={0}".format(w))
        w = yield w  # w接收send传进的数据,同时也是返回的数据
        print('[CONSUMER] Consuming %s...>> ', w)
        w *= len  # 将返回的数据乘以100
        time.sleep(0.1)


def consumer(coro):
    yield from coro  # 将数据传递到协程(生成器)对象中


def produce(c):
    c.send(None)  # "prime" the coroutine
    print("===================")
    for i in range(5):
        print('[Produce] Producing %s----', i)
        w = c.send(i)  # 发送完成后进入协程中执行
        print('[Produce] receive %s----', w)
    c.close()


c1 = consumer_work(100)
produce(consumer(c1))
# produce(c1)



import inspect
inspect.getgeneratorstate()

