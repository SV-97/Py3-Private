import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from time import time

import random
# find period of a function

x = sp.symbols("x")

#frequency1 = 12
#frequency2 = 18 # new frequency with 12,18 should be 6
frequency1 = random.randint(1, 13)/random.randint(1, 13)
frequency2 = random.randint(1, 13)/random.randint(1, 13)
offset = 0
print("frequency1 = {}".format(frequency1))
print("frequency2 = {}".format(frequency2))
print("offset = {}".format(offset))

f1 = sp.sin(2*sp.pi*frequency1*x+offset)
f2 = sp.sin(2*sp.pi*frequency2*x)
f3 = f1+f2
f1_l = sp.lambdify(x, f1)
f2_l = sp.lambdify(x, f2)
f3_l = sp.lambdify(x, f3)
for f in (f1_l, f2_l, f3_l):
    f = np.vectorize(f)
space = np.linspace(0, 26, 100e3)

def lcm(x1, x2): # can't use np.lcm because apparently "module 'numpy' has no attribute 'lcm'""
    lcm = 1
    while not (lcm/x1).is_integer() or not (lcm/x2).is_integer():
        lcm += 1
    else:
        return lcm

def gcd(x1, x2): # greatest common divisor
    if x1 <= x2:
        gcd = x1
    else:
        gcd = x2
    while not (x1/gcd).is_integer() or not (x2/gcd).is_integer():
        gcd -= 1
        if gcd <= 0:
            return None
    else:
        return gcd

frequency3 = gcd(frequency1, frequency2) 

plt.plot(space, f1_l(space), label = "f1 = {:.4e}Hz".format(frequency1), alpha = 0.5)
plt.plot(space, f2_l(space), label = "f2 = {:.4e}Hz".format(frequency2), alpha = 0.5)
plt.plot(space, f3_l(space), label = "f3 = {}".format("{:.4e}Hz".format(frequency3) if frequency3 != None else "Non-Periodic"))
plt.legend()
plt.show()