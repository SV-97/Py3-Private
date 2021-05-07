from model_wrapper import *


@solve_ivp(eulers_method, t_end=2000, step_size=10e-4)
@ivp(t_0=0.0, y_0=np.array((7.0, 3.0, 3.0)), a=10, b=28, c=8/3)
# @noise_multiplicative(random.gauss, mu=1, sigma=0.1)
# @noise_additive(random.gauss, mu=0, sigma=4)
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
alpha = -np.pi / 4
x, y = x*np.cos(alpha) - y * np.sin(alpha), x*np.sin(alpha) + y*np.cos(alpha)
mlab.plot3d(x, y, z, np.sqrt(distance_from_boundary **
                             2+r**2+b**2), colormap="afmhot")
input()
#ax = plt.axes(projection='3d')
## ax.plot3D(data["x"], data["y"], data["z"], linewidth=0.1)
#ax.scatter(data["x"], data["y"], data["z"], c=color)
#
# ax.grid(False)
# ax.set_xticks([])
# ax.set_yticks([])
# ax.set_zticks([])
#ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
#ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
#ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
# plot_everything(data)
#plt.subplot(4, 4, 12)
#plt.plot(ellipse_z, ellipse_y)

"""

def bifurcate(f, x_0, y, **params):
    x_n = x_0 * np.ones(y.shape)
    n_max = 50
    x_i = x_0 * np.ones((y.size, n_max))
    for n in range(n_max):
        x_n = f(x_n, y, **params)
        x_i[:, n] = x_n
    return np.column_stack([y, x_n, x_i])


def logistic_map(x, r):
    return r*x*(1-x)


sol = bifurcate(logistic_map, 0.5, np.linspace(3.6, 4, num=1000))
data = {"r": sol[:, 0], "x": sol[:, 1], "x_i": sol[:, 2:]}

ax = plt.axes(projection='3d')

for i in range(50):
    ax.plot3D(i * np.ones(data["r"].size), data["r"],
              data["x_i"][:, i], linewidth=0.5, alpha=0.5)
"""
# print(len(sol))
# plt.plot(sol[:, 0], sol[:, 1], linewidth=0.1)

# plt.get_current_fig_manager().window.showMaximized()
# plt.show()
