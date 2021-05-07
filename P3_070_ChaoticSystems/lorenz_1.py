import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d as plt3

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


@solve_ivp(eulers_method, t_end=1000, step_size=10e-3)
@ivp(t_0=0.0, y_0=np.array((7.0, 3.0, 3.0)), a=10, b=28, c=8/3)
# @noise_multiplicative(random.triangular)
# @noise_additive(random.uniform, a=-200, b=200)
def lorenz_system(t, x, a, b, c):
    [X, Y, Z] = x
    dx = a*(Y - X)
    dy = X*(b - Z) - Y
    dz = X*Y - c*Z
    return np.array([dx, dy, dz])


sol = lorenz_system()
data = {"time": sol.ts, "x": sol.ys[:, 0],
        "y": sol.ys[:, 1], "z": sol.ys[:, 2]}

x = data["x"]
y = data["y"]
z = data["z"]
one = np.ones(x.shape)
r = np.sqrt((x+8.5)**2+(y+8.49)**2+(z-27)**2)
g = np.sqrt((x)**2+(y)**2+(z-15)**2)
b = np.sqrt((x-8.5)**2+(y-8.49)**2+(z-27)**2)
#alpha = x
#alpha[:x.size] = np.abs(np.diff((x**2+y**2+z**2)))
#alpha[x.size-1] = alpha[-2]
a = 2*28
b = 50-4
z_0 = 4+b/2
y_0 = 0
phi = np.linspace(0, 2*np.pi)
ellipse_z = b/2*np.cos(phi) + z_0
ellipse_y = a/2*np.sin(phi) + y_0
distance_from_boundary = np.zeros(r.shape)
for i in range(z.size):
    distance_from_boundary[i] = np.amin(
        (z[i] - ellipse_z)**2 + (y[i] - ellipse_y)**2)
m = np.column_stack([(r+b)/2-z, distance_from_boundary,
                     (r+b)/2-z, distance_from_boundary])
m = np.abs(m)
color = m / np.amax(m)
ax = plt.axes(projection='3d')
# ax.plot3D(data["x"], data["y"], data["z"], linewidth=0.1)
ax.scatter(data["x"], data["y"], data["z"], linewidth=0.1, c=color)

ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))

plt.get_current_fig_manager().window.showMaximized()
plt.show()
