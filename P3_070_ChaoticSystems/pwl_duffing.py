from model_wrapper import *

i = -20


@solve_ivp(eulers_method, t_end=2500, step_size=10e-3)
@ivp(t_0=0.0, y_0=np.array((0.0, 0.0, 0.0)),
     e=.25,
     gamma=.14+i/20,
     m0=-0.845e-1,
     m1=.66,
     omega=1,
     c=.14+i/20)
# @noise_multiplicative(random.gauss, mu=0, sigma=0.1)
# @noise_additive(random.gauss, mu=0, sigma=0.1)
def pwl_duffing_mod(t, x, e, gamma, m0, m1, omega, c):
    [X, Y, Z] = x
    dx = Y
    dy = -m1*X-(m0 - m1)/2 * (np.abs(X + 1) - np.abs(X - 1)) - \
        e*Y + gamma * np.cos(omega*t)
    dz = 0.01
    return np.array([dx, dy, dz])


sol = pwl_duffing_mod()
data = {"time": sol.ts, "x": sol.ys[:, 0],
        "y": sol.ys[:, 1], "z": sol.ys[:, 2]}

x = data["x"]
y = data["y"]
z = data["z"]

print(np.amin(x), np.amax(x))
print(np.amin(y), np.amax(y))

xmin = np.amin(x)
x -= xmin + (np.amax(x) - xmin)/2
ymin = np.amin(y)
y -= ymin + (np.amax(y) - ymin)/2

r = x**2+y**2

mlab.plot3d(x, y, z, r, colormap="magma")
input()
