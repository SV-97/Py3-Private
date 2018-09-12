from time import time

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

# Getting a list of unique elements from a list

a = ["z","a","b","a","a","b","c","d","e","f","f","g","h","i","j","k","a","a","b","l","m","n","o","o","p","c","a","g"]
def method_1(a):
    t1 = time()
    b = list(set(a))
    t2 = time()
    del b
    return t2-t1

def method_2(a):
    t1 = time()
    b = []
    for element in a:
        if element not in b:
            b.append(element)
    t2 = time()
    del b
    return t2-t1

times_1 = []
times_2 = []
for i in range(10000):
    times_1.append(method_1(a))
    times_2.append(method_2(a))

def average(a):
    return sum(a)/len(a)
average_1 = average(times_1)
average_2 = average(times_2)

times_1_1 = [time for time in times_1 if time <= 2*average_1]
times_2_1 = [time for time in times_2 if time <= 1.5*average_2]
average_1_1 = average(times_1_1)
average_2_1 = average(times_2_1)
plt.suptitle("Speed comparison set-conversion vs for-loop", fontsize = 16)
plt.subplot(2,1,2)
plt.title("Sanitized")
plt.plot(range(len(times_1_1)), times_1_1, label = "method 1: {}".format(average_1_1))
plt.plot(range(len(times_2_1)), times_2_1, label = "method 2: {}".format(average_2_1))
plt.ylabel("time/s")
plt.xlabel("iteration")
plt.ticklabel_format(style="sci", axis="y", scilimits=(0,0))
plt.legend()

plt.subplot(2,1,1)
plt.title("Unsanitized")
plt.plot(range(10000), times_1, label = "method 1: {}".format(average_1))
plt.plot(range(10000), times_2, label = "method 2: {}".format(average_2))
plt.ylabel("time/s")
plt.xlabel("iteration")
plt.ticklabel_format(style="sci", axis="y", scilimits=(0,0))
plt.legend()
plt.show()
