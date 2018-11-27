# coding: utf-8
# __author__: ""


def lazy_range(up_to):
    """Generator to return the sequence of integers from 0 to up_to, exclusive."""
    index = 0

    def gratuitous_refactor():
        nonlocal index
        while index < up_to:
            yield index
            index += 1

    yield from gratuitous_refactor()


gennerator = lazy_range(10)
print(type(gennerator))

# print(next(gennerator))  # 0
print(next(gennerator))  # 0
print(next(gennerator))  # 0
print(next(gennerator))  # 0
#
print(gennerator.send(2))  # 2
print(next(gennerator))  # 3
# print(gennerator.send(-1))  # 2

# for x in gennerator:
#     print(x)  # 3, 4


