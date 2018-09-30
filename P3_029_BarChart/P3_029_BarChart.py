import collections
import matplotlib.pyplot as plt

l = ['a', 'b', 'b', 'b', 'c']
count = collections.Counter(l)
elements = plt.bar(count.keys(), count.values())

for i in range(len(elements)):
    elements[i].set_facecolor((i/len(elements), 0.3, 0.9))
plt.grid(axis="y")
plt.show()