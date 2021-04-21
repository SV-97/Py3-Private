import numpy as np
import matplotlib.pyplot as plt

from math import exp, sqrt, log
from timeit import timeit
from functools import wraps
from typing import Callable, Dict
import random

from odes import solve_ivp, eulers_method, ivp

random.seed(10)


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
                plt.plot(x[0], y[0], "x", color="tab:blue", label="start")
                plt.plot(x[-1], y[-1], "x", color="tab:orange", label="end")
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


cbr = 18.5  # crude birth rate value for 2015-2020 from wikipedia https://en.wikipedia.org/wiki/Birth_rate
cdr = 7.7  # crude death rate estimate for 2020 from wikipedia https://en.wikipedia.org/wiki/Mortality_rate


@solve_ivp(eulers_method, t_end=100, step_size=10e-3)
@ivp(t_0=0.0, y_0=np.array((7.0, 3.0, 3.0)),
     birth_rate=cbr * 1e-3 / 1e9,
     death_rate=cdr * 1e-3 / 1e9,
     pollution_rate=0.001,
     recovery_rate=0.002,
     sol_growth_rate=0.01,
     sol_decrease_rate=0.05,
     l_tip=1.0,
     environmental_death_rate=cdr*1e-3*0.2
     )
@noise_multiplicative(random.gauss, mu=0.01, sigma=0.2)
@noise_additive(random.uniform, a=-0.2, b=0.4)
def world_model(t, x, birth_rate,
                death_rate,
                pollution_rate,
                recovery_rate,
                sol_growth_rate,
                sol_decrease_rate,
                l_tip,
                environmental_death_rate):
    [b, l, u] = x
    db = ((birth_rate - death_rate) * l/u - environmental_death_rate*u) * b
    du = -u*(recovery_rate - pollution_rate*b) - \
          l*exp(-(l - l_tip)**2)
    dl = sol_growth_rate * b / l - sol_decrease_rate * \
        u * l
    if t < 10e-6:
        print(l*exp(-(l - l_tip)**2))
    #print(db, du, dl)
    return np.array([db, dl, du])


sol = world_model()
data = {"time": sol.ts, "population": sol.ys[:, 0],
        "pollution": sol.ys[:, 1], "standart of living": sol.ys[:, 2]}

plot_everything(data)
plt.get_current_fig_manager().window.showMaximized()
plt.show()
