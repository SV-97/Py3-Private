from main import uniform_distribution, take
from itertools import count
import numpy as np
from datetime import timedelta
from random import uniform, seed
from multiprocessing import Pool
from statistics import mean

runs = 150
n_procs = 8

lam = 1e-6
delta_t = (1/lam) / 3e4
#lambda_2 = 4.88e-18

p = lam*delta_t

N_0 = 5_000
runs_per_process = runs // n_procs


def simulation(rank):
    u = uniform_distribution()  # uniform
    ns = []
    seed(rank)
    for run in range(runs_per_process):
        print(f"Rank {rank} @ run {run}")
        N = N_0
        for t in count(0):
            #print(t, N)
            #zs = np.array(list(take(u, N)))
            zs = np.array([u(0, 1) for _ in range(N)])
            k = np.sum(zs < p)
            N -= k
            if N < N_0 / 2:
                n_exit = t
                break
        ns.append(n_exit)
    print(ns)
    return mean(ns)


if __name__ == "__main__":
    with Pool(n_procs) as p:
        ns = p.map(simulation, range(8))
        T = timedelta(seconds=mean(ns) * delta_t)
        print(f"T = {T}")

#print(f"T = {T}")
"""
[20414, 20341, 20741, 19886, 21017, 20427, 21250, 20097, 20590, 20349, 20853, 20890, 20377, 20532, 21181, 21015, 20516, 20169]
[20386, 20178, 20901, 20523, 20933, 20327, 21629, 20545, 20667, 21026, 20691, 20201, 21029, 20736, 20667, 21008, 20529, 21264]
[21271, 20981, 20852, 20210, 20489, 20707, 20070, 20622, 21061, 20334, 20838, 21129, 20909, 21056, 21135, 20865, 20756, 21135]
[20442, 21620, 21101, 21001, 20572, 21365, 20882, 20281, 20542, 20282, 21083, 20167, 20325, 21299, 21333, 20453, 21036, 20378]
[20095, 20919, 20605, 21635, 20549, 20451, 21325, 20468, 20497, 21041, 20913, 20657, 21050, 20614, 21424, 20800, 21239, 20375]
[20594, 21069, 21355, 21546, 20942, 21638, 20986, 21165, 21049, 20204, 21733, 20357, 20385, 20534, 21166, 21405, 20485, 20547]
[20537, 20063, 21838, 21056, 21079, 20815, 20396, 20496, 20495, 21405, 20846, 20332, 20868, 20480, 20547, 20827, 21643, 21151]
[21417, 20802, 19878, 20502, 21116, 20297, 21136, 20589, 21183, 21190, 20390, 20906, 21218, 20853, 20626, 20912, 20502, 21393]
T = 8 days, 0:31:11.296296
"""
