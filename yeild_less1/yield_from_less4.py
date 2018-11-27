# coding: utf-8
# __author__: ""


'''
代码变量说明:
_i 迭代器（子生成器）
_y 产出的值 （子生成器产出的值）
_r 结果 （最终的结果 即整个yield from表达式的值）
_s 发送的值 （调用方发给委派生成器的值，这个只会传给子生成器）
_e 异常 （异常对象）


RESULT = yield from EXPR   伪代码实现
'''


def test():
    EXPR = range(100)

    # is semantically equivalent to
    # EXPR 可以是任何可迭代对象，因为获取迭代器_i 使用的是iter()函数。
    _i = iter(EXPR)

    _y = next(_i)  # 2 预激字生成器，结果保存在_y 中，作为第一个产出的值

    while 1:  # 4 运行这个循环时，委派生成器会阻塞，只能作为调用方和子生成器直接的通道

        _s = yield _y  # 5 产出子生成器当前产出的元素；等待调用方发送_s中保存的值。

        try:  # 10 尝试让子生成器向前执行
            if _s is None:
                # 11. 如果发送的值是None，那么会调用子生成器的 __next__()方法。
                _y = next(_i)
            else:
                # 11. 如果发送的值不是None，那么会调用子生成器的send()方法。
                _y = _i.send(_s)
        except StopIteration as _e:  # 12
            # 2. 如果调用的方法抛出StopIteration异常，获取异常对象的value属性，赋值给_r, 退出循环，委派生成器恢复运行。任何其他异常都会向上冒泡，传给委派生成器。
            _r = _e.value
            break

    RESULT = _r  # 13 返回的结果是 _r 即整个yield from表达式的值
    return RESULT


