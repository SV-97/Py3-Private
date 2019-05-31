from statistics import median
from string import ascii_letters
import tempfile
from time import time

with tempfile.TemporaryFile("w+") as out:
    def printer(a):
        print(a, file=out)

    def f_1(a):
        for b in a:
            printer(b)

    def f_2(a):
        # for _ in (printer(b) for b in a): pass is terribly slow in comparison
        [printer(b) for b in a]

    def f_3(a):
        for _ in map(printer, a): pass

    for j in range(10):
        T1 = []
        T2 = []
        T3 = []
        a = [a for a in ascii_letters]
        for i in range(2000):
            t1 = time()
            f_1(a);
            t2 = time()
            T1.append(t2 - t1)

            t1 = time()
            f_2(a);
            t2 = time()
            T2.append(t2 - t1)

            t1 = time()
            f_3(a);
            t2 = time()
            T3.append(t2 - t1)

        print(f"#{j}")
        times = {key: median(val) for key, val in zip(("For loop", "List Comprehension", "Map"), (T1, T2, T3))}
        for key, val in times.items():
            print(f"{key}: {val:.4e}")
        min_ = min(map(median, (T1, T2, T3)))
        fastest = {val: key for key, val in times.items()}[min_]
        print(f"Fastest was {fastest}")