import multiprocessing
import os
import re
from time import time

import matplotlib.pyplot as plt

def str_n(i):
    return str(i)+"\n"
def _faculty(range_):
    x = 1
    for i in range_:
        x *= i
    return x

def faculty(n, number_of_processes=4):
    def _faculty(range_):
        x = 1
        for i in range_:
            x *= i
        return x
    class PartialFaculty(multiprocessing.Process):
        def __init__(self, queue, range_):
            super().__init__()
            self.queue = queue
            self.range = range_
        def run(self):
            x = _faculty(self.range)
            self.queue.put(x)
            self.queue.close()
    def distribute(lst, n):
        """distributes lst as equal as possible to n elements
        """
        base_load = len(lst)//n
        extra_load = len(lst)%n
        load_per_element = [base_load for i in range(n)]
        for i in range(len(load_per_element)):
            if extra_load <= 0: break
            load_per_element[i] +=  1 if extra_load > 0 else 0
            extra_load -= 1
        indexes = [sum(load_per_element[:i+1]) for i in range(n)]
        indexes.insert(0, None) #added so that slicing can be used
        indexes.append(None)
        elements = [lst[indexes[i]:indexes[i+1]] for i in range(n)]
        return elements
        
    ranges = distribute(range(1,n+1), number_of_processes)

    queue = multiprocessing.Queue()
    processes = [PartialFaculty(queue, range_) for range_ in ranges]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    part_results = [queue.get() for i in range(number_of_processes)]
    return _faculty(part_results)

if __name__ == "__main__":
    vals = range(10000)
    procs = range(2,7)
    T1 = {i:[] for i in procs}
    T2 = []
    path = os.path.dirname(__file__)
    files = os.listdir(path)
    time_files = re.findall(r"times[0-9]+", "".join(files))
    if not time_files:
        for n in vals:
            print(n)
            for i in procs:
                t1 = time()
                a = faculty(n, i)
                t2 = time()
                T1[i].append(t2-t1)
            t3 = time()
            b = _faculty(range(1,n+1))
            t4 = time()
            T2.append(t4-t3)
        for key in T1:
            with open(path+"/times1"+str(key), "w") as f:
                f.writelines(map(str_n, T1[key]))
        with open(path+"/times2", "w") as f:
            f.writelines(map(str_n, T2))
    else:
        with open(path+"/times2", "r") as f:
            content = f.readlines()
            T2 = map(float, content)
        for i in procs:
            with open(path+"/times1"+str(i), "r") as f:
                content = f.readlines()
                T1[i] = map(float, content)

    plt.plot(vals, list(T2), label="1 process", drawstyle="steps")
    for key in T1:
        plt.plot(vals, list(T1[key]), label="{} processes".format(key), drawstyle="steps")
    
    plt.title("n!")
    plt.ylabel("time/s")
    plt.xlabel("n")
    plt.suptitle("Speed comparison between parallel solution with varying number of processes vs. linear")

    plt.legend()
    plt.grid()
    plt.show()