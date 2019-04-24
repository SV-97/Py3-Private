from math import pi, sin
from time import time
import matplotlib.pyplot as plt

import rusty_integration as ri
import string_sum as ss

def dbg(x):
    print(f"{x:<10} {str(eval(x)):<15}")

def f(x):
    return sin(x)

print()

a = ss.sum_as_string(1, 5)
dbg("a")
dbg("type(a)")
print()

ri.external_call(lambda : print("Hello World"))
print()

b = ri.ext_call_ret(lambda : 42)
dbg("b")
dbg("type(b)")
print()
 
def exception():
    raise ValueError("Test Error")
try:
    c = ri.ext_call_ret(lambda : exception())
except ValueError as e:
    print("Exception: ", e)
else:
    dbg("c")
    dbg("type(c)")
print()

ri.ext_call_arg(lambda s: print(s), "test")
print()

d = ri.ext_add(1, 2)
dbg("d")
dbg("type(d)")
print()

e = ri.composite_simpsons(f, -pi, pi, int(100e3))
dbg("e")
dbg("type(e)")

T1 = []
T2 = []
n = list(range(100))
for i in n:
    t1 = time()
    e = ri.composite_simpsons(f, -pi, pi, int(100e3))
    t2 = time()
    e = ri.alternative_composite_simpsons(f, -pi, pi, int(100e3))
    t3 = time()
    T1.append(t2-t1)
    T2.append(t3-t2)

plt.plot(n, T1, label="External GIL")
plt.plot(n, T2, label="Internal GIL")
plt.legend()
plt.show()