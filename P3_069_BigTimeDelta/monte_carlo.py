from main import uniform_distribution, take
from big_timedelta import BigTimeDelta

from itertools import count
from datetime import timedelta
from random import uniform, seed
from multiprocessing import Pool, Barrier, Lock
from statistics import mean

import numpy as np
from tqdm import trange, tqdm

N_PROCS = 8

IOD = "Iodine-131"
URAN = "Uranium-238"
ELEMENT = IOD

EXACT = {
    IOD: BigTimeDelta(days=8.0252),
    URAN: BigTimeDelta(years=4.47e9)
}

if ELEMENT == IOD:
    RUNS = 150
    LAM = 1e-6
    N_0 = 100
elif ELEMENT == URAN:
    RUNS = 200
    LAM = 4.88e-18
    N_0 = 100

DELTA_T = (1/LAM) / 3e4
P = LAM*DELTA_T
# could use a better chunking strategy and map over zip(ranks, n_runs_for_rank) but eh
RUNS_PER_PROCESS = RUNS // N_PROCS


def simulation(rank):
    global lock
    global barrier
    u = uniform_distribution(seed=rank)
    ns = []
    p = P

    with lock:
        pbar = tqdm(total=RUNS_PER_PROCESS,
                    desc=f"Process {rank: >2}", unit="run", position=rank, ncols=100)
    for _run in range(RUNS_PER_PROCESS):
        n = N_0
        n_0 = N_0
        for t in count(0):
            zs = np.array(list(take(u, n)))
            # count how many random numbers are less than p
            k = np.sum(zs < p)
            n -= k
            if n < n_0 / 2:
                n_exit = t
                break
        ns.append(n_exit)
        pbar.update()
    barrier.wait()
    pbar.close()
    barrier.wait()
    with lock:
        print(ns)
    return mean(ns)


def pool_init(b, l):
    global barrier
    global lock
    global done
    done = 0
    barrier = b
    lock = l


if __name__ == "__main__":
    b = Barrier(N_PROCS)
    l = Lock()
    with Pool(N_PROCS, initializer=pool_init, initargs=(b, l)) as p:
        ns = p.map(simulation, range(N_PROCS))
        time_in_seconds = mean(ns) * DELTA_T
        T = BigTimeDelta(seconds=time_in_seconds)
        print(f"\n{ELEMENT}\nT = {T}\n  = {T:.2f}\n  = {time_in_seconds} seconds")
        f = (1 - float(EXACT[ELEMENT].in_nanos / T.in_nanos)) * 100
        print(f"relative error: {f:.2f}%")


""" Iodine-131
Process  2: 100%|██████████████████████████████████████████████████| 18/18 [00:39<00:00,  2.20s/run]
Process  4: 100%|██████████████████████████████████████████████████| 18/18 [00:39<00:00,  2.20s/run]
Process  5: 100%|██████████████████████████████████████████████████| 18/18 [00:39<00:00,  2.20s/run]
Process  6: 100%|██████████████████████████████████████████████████| 18/18 [00:39<00:00,  2.20s/run]
Process  3: 100%|██████████████████████████████████████████████████| 18/18 [00:39<00:00,  2.20s/run]
Process  0: 100%|██████████████████████████████████████████████████| 18/18 [00:39<00:00,  2.20s/run]
Process  7: 100%|██████████████████████████████████████████████████| 18/18 [00:39<00:00,  2.20s/run]
Process  1: 100%|██████████████████████████████████████████████████| 18/18 [00:39<00:00,  2.20s/run]
[24996, 24014, 14242, 21946, 24570, 20793, 17979, 22460, 19093, 20640, 18297, 11836, 18843, 21391, 19940, 20338, 20654, 18905]
[21825, 25987, 17282, 20926, 20960, 18684, 20183, 18738, 18420, 20233, 19235, 19257, 20195, 22381, 22519, 21726, 23836, 16787]
[20610, 24430, 19181, 21292, 17239, 19535, 24591, 21777, 17487, 24533, 19213, 15588, 16927, 24941, 25262, 19955, 17273, 21779]
[21811, 19196, 19000, 21371, 21706, 23743, 20598, 18630, 19847, 20709, 20588, 19349, 22434, 21257, 21177, 28932, 21855, 20003]
[25335, 19411, 26089, 18392, 17615, 23879, 20286, 18966, 25223, 24271, 22589, 18855, 19028, 20455, 21312, 21055, 29100, 20295]
[20778, 22250, 20986, 23005, 18545, 21979, 21216, 20890, 29714, 21063, 20664, 21091, 20357, 21168, 18835, 24419, 23170, 22356]
[25149, 16773, 16742, 19707, 20400, 19692, 18906, 23332, 22977, 16186, 24085, 19889, 20062, 25012, 24301, 21354, 14916, 20838]
[22826, 22277, 22520, 22833, 20172, 19838, 18909, 18922, 24166, 19837, 15661, 23510, 20977, 26330, 24765, 23918, 18021, 26094]

Iodine-131
T = 701497/86400 days, 27 millis, 222 micros, 1864195875/8388608 nanos
  = 8.12 days, 27.00 millis, 222.00 micros, 222.23 nanos
  = 701497.4537037038 seconds
relative error: 1.16%
"""
""" Uranium-238
Process  4: 100%|██████████████████████████████████████████████████| 25/25 [00:54<00:00,  2.18s/run]
Process  5: 100%|██████████████████████████████████████████████████| 25/25 [00:54<00:00,  2.18s/run]
Process  0: 100%|██████████████████████████████████████████████████| 25/25 [00:54<00:00,  2.19s/run]
Process  6: 100%|██████████████████████████████████████████████████| 25/25 [00:54<00:00,  2.18s/run]
Process  4: 100%|██████████████████████████████████████████████████| 25/25 [00:54<00:00,  1.56s/run]
Process  2: 100%|██████████████████████████████████████████████████| 25/25 [00:54<00:00,  2.18s/run]
Process  7: 100%|██████████████████████████████████████████████████| 25/25 [00:54<00:00,  2.18s/run]
Process  1: 100%|██████████████████████████████████████████████████| 25/25 [00:54<00:00,  2.18s/run]
[21825, 25987, 17282, 20926, 20960, 18684, 20183, 18738, 18420, 20233, 19235, 19257, 20195, 22381, 22519, 21726, 23836, 16787, 22893, 17083, 22861, 21345, 21353, 20434, 23053]
[21811, 19196, 19000, 21371, 21706, 23743, 20598, 18630, 19847, 20709, 20588, 19349, 22434, 21257, 21177, 28932, 21855, 20003, 23320, 21154, 18512, 22578, 21152, 22322, 19992]
[20610, 24430, 19181, 21292, 17239, 19535, 24591, 21777, 17487, 24533, 19213, 15588, 16927, 24941, 25262, 19955, 17273, 21779, 21765, 25896, 22920, 23819, 22435, 18389, 21687]
[25335, 19411, 26089, 18392, 17615, 23879, 20286, 18966, 25223, 24271, 22589, 18855, 19028, 20455, 21312, 21055, 29100, 20295, 20666, 26465, 24387, 25819, 18698, 18852, 19762]
[22826, 22277, 22520, 22833, 20172, 19838, 18909, 18922, 24166, 19837, 15661, 23510, 20977, 26330, 24765, 23918, 18021, 26094, 22801, 24213, 27063, 17616, 19994, 22141, 24543]
[25149, 16773, 16742, 19707, 20400, 19692, 18906, 23332, 22977, 16186, 24085, 19889, 20062, 25012, 24301, 21354, 14916, 20838, 20240, 24473, 17049, 23204, 23887, 19498, 17462]
[20778, 22250, 20986, 23005, 18545, 21979, 21216, 20890, 29714, 21063, 20664, 21091, 20357, 21168, 18835, 24419, 23170, 22356, 25078, 22405, 29613, 21916, 20382, 21575, 20181]
[24996, 24014, 14242, 21946, 24570, 20793, 17979, 22460, 19093, 20640, 18297, 11836, 18843, 21391, 19940, 20338, 20654, 18905, 22117, 18464, 19093, 14677, 18372, 23589, 20460]

Uranium-238
T = 4527607368510929/985500000 millenia
  = 4594223.61 millenia
  = 1.4488343579234973e+17 seconds
relative error: 2.70%
"""
