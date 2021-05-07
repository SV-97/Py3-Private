import numpy as np
import matplotlib.pyplot as plt
from mayavi import mlab

from math import exp, sqrt, log
from timeit import timeit
from functools import wraps
from typing import Callable, Dict
import random

from odes import solve_ivp, eulers_method, ivp

random.seed(10)
plt.style.use("dark_background")


def plot_everything(data: Dict[str, np.array]):
    n = len(data)
    for (i, (x_lbl, x)) in enumerate(data.items()):
        for (j, (y_lbl, y)) in enumerate(data.items()):
            plt.subplot(n, n, j*n+i + 1)
            if i == j:
                plt.text(0.3, 0.3, x_lbl, fontsize="large", fontweight="bold")
                plt.axis("off")
            else:
                plt.plot(x, y)
                plt.plot(x[0], y[0], "x", color="tab:blue",
                         label="start", linewidth=0.1)
                plt.plot(x[-1], y[-1], "x", color="tab:orange",
                         label="end", linewidth=0.1)
                plt.legend()


def noise(g: Callable[[np.array, Callable[[], float]], np.array]):
    def noised_f(noise: Callable, **noise_args):
        def wrapper(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                return g(f(*args, **kwargs), lambda: noise(**noise_args))
            return wrapped
        return wrapper
    return noised_f


noise_additive = noise(lambda fx, n: fx + n())
noise_multiplicative = noise(lambda fx, n: fx*n())
