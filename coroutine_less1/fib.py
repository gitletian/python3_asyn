# coding: utf-8
# __author__: ""

import time
now = lambda: int(time.time())


def fib_(n):
    return fib_(n - 1) + fib_(n - 2) if n > 1 else n


def log_execution_time(n):
    '''

    :param func:
    :return:
    '''
    t1 = now()
    fib_(n)

    print("===========耗时===={0}".format(now() - t1))
    return now() - t1


timed_fib = lambda n: log_execution_time(n)

# print(timed_fib(39))


