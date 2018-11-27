# coding: utf-8
# __author__: ""

'''
send 和 next 都一样
只是 send 可以 重置 yield 表达式的返回值,
send(None) 相当于 next

'''


def fun():
    print('start...')
    m = yield 5
    print(m)
    print('middle...')
    d = yield 12
    print(d)
    print('end...')

g1 = fun()
print("==============")
print(next(g1))

print(g1.send('message'))
print("==============")
print(next(g1))
