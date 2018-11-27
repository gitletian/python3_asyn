# coding: utf-8
# __author__: ""


'''
委派生成器在 yield from 表达式处暂停时，调用方可以直接把数据发给子生成器，
子生成器再把产出的值发给调用方。
子生成器返回之后，解释器会抛出StopIteration 异常，并把返回值附加到异常对象上，此时委派生成器会恢复。

grouper 发送的每个值都会经由 yield from 处理，通过管道传给 averager 实例。
grouper 会在 yield from 表达式处暂停，等待 averager 实例处理客户端发来的值。
averager 实例运行完毕后，返回的值绑定到 results[key] 上。
while 循环会不断创建 averager 实例，处理更多的值。

外层 for 循环重新迭代时会新建一个 grouper 实例，然后绑定到 group 变量上。
前一个 grouper 实例（以及它创建的尚未终止的 averager 子生成器实例）被垃圾回收程序回收。

这个试验想表明的关键一点是，如果子生成器不终止，委派生成器会在yield from 表达式处永远暂停。
如果是这样，程序不会向前执行，因为 yield from（与 yield 一样）把控制权转交给客户代码（即，委派生成器的调用方）了。



PEP 380 在“Proposal”一节（https://www.python.org/dev/peps/pep-0380/#proposal）分六点说明了 yield from 的行为。
这里几乎原封不动地引述，不过把有歧义的“迭代器”一词都换成了“子生成器”，还做了进一步说明。上面的示例阐明了下述四点：

1、子生成器产出的值都直接传给委派生成器的调用方（即客户端代码）；
2、使用 send() 方法发给委派生成器的值都直接传给子生成器。如果发送的值是None，那么会调用子生成器的 __next__() 方法。
   如果发送的值不是 None，那么会调用子生成器的 send() 方法。
   如果子生成器抛出 StopIteration 异常，那么委派生成器恢复运行。任何其他异常都会向上冒泡，传给委派生成器；

3、生成器退出时，生成器（或子生成器）中的 return expr 表达式会触发 StopIteration(expr) 异常抛出；
4、yield from 表达式的值是子生成器终止时传给 StopIteration 异常的第一个参数。

yield from 的行为:
1、子生成器产出的值都直接传给委派生成器的调用方（客户端代码）
2、使用send() 方法发给委派生成器的值都直接传给子生成器。如果发送的值是None，那么会调用子生成器的 next()方法。如果发送的值不是None，那么会调用子生成器的send()方法。如果调用的方法抛出StopIteration异常，那么委派生成器恢复运行。任何其他异常都会向上冒泡，传给委派生成器。
3、生成器退出时，生成器（或子生成器）中的return expr 表达式会触发 StopIteration(expr) 异常抛出。
4、yield from表达式的值是子生成器终止时传给StopIteration异常的第一个参数。
5、传入委派生成器的异常，除了 GeneratorExit 之外都传给子生成器的throw()方法。如果调用throw()方法时抛出 StopIteration 异常，委派生成器恢复运行。StopIteration之外的异常会向上冒泡。传给委派生成器。
6、如果把 GeneratorExit 异常传入委派生成器，或者在委派生成器上调用close() 方法，那么在子生成器上调用close() 方法，如果他有的话。如果调用close() 方法导致异常抛出，那么异常会向上冒泡，传给委派生成器；否则，委派生成器抛出 GeneratorExit 异常。

'''

from collections import namedtuple

Result = namedtuple('Result', 'count average')


# 子生成器
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        # main 函数发送数据到这里
        print("in averager, before yield")
        term = yield
        if term is None:  # 终止条件
            break
        total += term
        count += 1
        average = total/count

    print("in averager, return result")
    return Result(count, average)  # 返回的Result 会成为grouper函数中yield from表达式的值


# 委派生成器
def grouper(results, key):
    #  这个循环每次都会新建一个averager 实例，每个实例都是作为协程使用的生成器对象
    while True:
        print("in grouper, before yield from averager, key is ", key)
        results[key] = yield from averager()
        print("in grouper, after yield from, key is ", key)


# 委派生成器
# def grouper(results, key):
#     #  这个循环每次都会新建一个averager 实例，每个实例都是作为协程使用的生成器对象
#     print("in grouper, before yield from averager, key is ", key)
#     results[key] = yield from averager()
#     print("in grouper, after yield from, key is ", key)
#     print(results)


# 调用方
def main(data):
    results = {}
    for key, values in data.items():
        # group 是调用grouper函数得到的生成器对象
        group = grouper(results, key)
        print("\ncreate group: ", group)

        next(group)  # 预激 group 协程。
        print("pre active group ok")

        for value in values:
            # 把各个value传给grouper 传入的值最终到达 averager 函数中；
            # grouper并不知道传入的是什么，同时grouper实例在yield from处暂停
            print("send to %r value %f now" % (group, value))
            group.send(value)
        # 把None传入groupper，传入的值最终到达averager函数中，导致当前实例终止。然后继续创建下一个实例。
        # 如果没有group.send(None)，那么averager子生成器永远不会终止，委派生成器也永远不会在此激活，也就不会为result[key]赋值
        print("send to %r none" % group)
        group.send(None)
    print("report result: ")
    report(results)


# 输出报告
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(result.count, group, result.average, unit))


data = {
    'girls;kg': [40, 41, 42, 43, 44, 54],
    'girls;m': [1.5, 1.6, 1.8, 1.5, 1.45, 1.6],
    'boys;kg': [50, 51, 62, 53, 54, 54],
    'boys;m': [1.6, 1.8, 1.8, 1.7, 1.55, 1.6],
}

if __name__ == '__main__':
    main(data)

