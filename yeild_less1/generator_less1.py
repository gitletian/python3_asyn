# coding: utf-8
# __author__: ""


def jumping_range(up_to):
    """Generator for the sequence of integers from 0 to up_to, exclusive.
    Sending a value into the generator will shift the sequence by that amount.
    """
    index = 0
    while index < up_to:
        jump = yield index
        print("========={0}".format(jump))
        if jump is None:
            jump = 1
        index += jump


if __name__ == '__main__':

    gennerator = jumping_range(10)

    print(next(gennerator))  # 0
    print(next(gennerator))  # 0
    print(next(gennerator))  # 0
    print(next(gennerator))  # 0

    print(gennerator.send(2))  # 2
    print(next(gennerator))  # 3
    print(gennerator.send(-1))  # 2

    for x in gennerator:
        print(x)  # 3, 4