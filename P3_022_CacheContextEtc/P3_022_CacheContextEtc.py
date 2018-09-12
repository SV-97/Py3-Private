
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

import contextlib
import functools
import time

###

@contextlib.contextmanager
def runtime():
    t1 = time.perf_counter()
    try:
        yield
    finally:
        print("Runtime: {:.2f}s".format(time.perf_counter() - t1))

b = []
with runtime():
    for i in np.linspace(1,10,200e3):
        b.append(np.exp(i))

with runtime():
    for i in range(10):
        b = []
        for i in np.linspace(1,10,200e3):
            b.append(np.exp(i))

### partially evaluated function

def function(a,b,c,d):
    return 2*a+3*b+4*c+5*d
function_partial = functools.partial(function, 1, 3, 5)
# equal to
def function_partial_2(d):
    return 2*1+3*3+4*5+5*d

print(function_partial(2))

### function with cache

@functools.lru_cache(5)
def cached_f(a,b):
    return a+b

a = [cached_f(i,1) for i in range(5)]
b = cached_f(1,1)
print(cached_f.cache_info())
cached_f.cache_clear()
print(cached_f.cache_info())