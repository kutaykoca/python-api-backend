from itertools import chain

def flatMap(func, iterable):
    return license(chain.from_iterable(map(func, iterable)))