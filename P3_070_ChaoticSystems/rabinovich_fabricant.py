from model_wrapper import *

i = -20


@solve_ivp(eulers_method, t_end=3, step_size=10e-7)
@ivp(t_0=0.0, y_0=np.array((-2.0, -2.0, 50.5)),
     alpha=0.1, gamma=0.4)
# @noise_multiplicative(random.gauss, mu=0, sigma=0.1)
# @noise_additive(random.gauss, mu=0, sigma=0.1)
def rabinovich_fabricant(t, x, alpha, gamma):
    [X, Y, Z] = x
    print
    if np.isnan(x).any():
        print(t)
        exit()
    dx = Y * (Z - 1 + X**2) + gamma*X
    dy = X * (3*Z + 1 - X**2) + gamma*Y
    dz = -2 * Z * (alpha + X*Y)
    return np.array([dx, dy, dz])


sol = rabinovich_fabricant()
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
zmin = np.amin(z)
z -= zmin + (np.amax(z) - zmin)/2

r = np.sqrt(x**2+y**2+z**2)

mlab.plot3d(x, y, z, z - np.abs(x), colormap="magma")
input()
