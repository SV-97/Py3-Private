import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from time import time

class Source():
    def __init__(self, voltage):
        self.voltage = voltage

sources = [Source(i) for i in range(500)]
iterations = int(10e3)
# Comprehension Approach
times1 = []
for i in range(0,iterations):
    t1 = time()
    voltages = [source.voltage for source in sources]
    for voltage in voltages:
        a = voltage+1
    t2 = time()
    del voltages
    times1.append(t2-t1)

# Iterator Approach
times2 = []
for i in range(0,iterations):
    t1 = time()
    class Iterator():
        def __init__(self, sources):
            self.start = 0
        def __iter__(self):
            i = self.start
            e = len(sources)-1
            while i < e:
                yield sources[i].voltage
                i += 1

    for voltage in Iterator(sources):
        a = voltage+1
    t2 = time()
    del Iterator
    times2.append(t2-t1)
avrg1 = sum(times1)/len(times1)
deviation1 = []
for time in times1:
    deviation1.append(time-avrg1)
standart_deviation1 = sum(deviation1)/len(deviation1)
avrg2 = sum(times2)/len(times2)
deviation2 = []
for time in times2:
    deviation2.append(time-avrg2)
standart_deviation2 = sum(deviation2)/len(deviation2)

x_minus = 0

times2_working = times2[:]
for i in range(len(times2)):
    if abs(times2[i] - standart_deviation2) > abs(5e16*standart_deviation2):
        print("{:.2e} and {:.2e}".format(abs(times2[i] - standart_deviation2)/standart_deviation2, 5e8*standart_deviation2))
        times2_working.remove(times2[i])
        x_minus += 1
times2 = times2_working

avrg2 = sum(times2)/len(times2)
deviation2 = []
for time in times2:
    deviation2.append(time-avrg2)
standart_deviation2 = sum(deviation2)/len(deviation2)

plt.subplot(2,1,1)
x = np.linspace(0, iterations, iterations)
plt.plot(x,times1, label = "List Comprehension")
av_x = [x[0],x[-1]]
av_y = [avrg1, avrg1]
plt.plot(av_x, av_y, label = "Average")
plt.title("Average for comprehension is {:.4e}s with standart deviation of {:.4e}s".format(avrg1, standart_deviation1))
plt.legend()

plt.subplot(2,1,2)
x = np.linspace(0, iterations-x_minus, iterations-x_minus)
plt.plot(x,times2, label = "Custom Iterator")
av_x = [x[0],x[-1]]
av_y = [avrg2, avrg2]
plt.plot(av_x, av_y, label = "Average")
plt.title("Average for custom iterator is {:.4e}s with standart deviation of {:.4e}s".format(avrg2, standart_deviation2))
plt.legend()

plt.show()

9e14