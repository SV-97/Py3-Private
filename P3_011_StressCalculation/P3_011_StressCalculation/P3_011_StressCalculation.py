
import numpy as np
import timeit as t
import matplotlib.pyplot as plt
from scipy.integrate import simps
plt.xkcd()

a = 3454.62
b = 316.229
epsilon = 0.3 # Poissonzahl
sigma_z_max = 19760 # sigma_z_max
k = a/b
mean = np.arctan(a/z)

z = np.arange(0,1000+1,1)
print("z = {}".format(z))
#@np.vectorize(otypes=[float])
def T(a,b,z):
    return np.sqrt((b**2+z**2)/(a**2+z**2))
T = np.vectorize(T, otypes=[np.float])

def sigma_z(e, sigma_z_max, a, T):
    return -sigma_z_max*(b/(e**2*a))*((1-T**2)/T)
sigma_z = np.vectorize(sigma_z, otypes=[np.float])

T_val = T(a,b,z)
print("T = {}".format(T_val))

sigma_z_val = sigma_z(epsilon, sigma_z_max, a, T_val)

integral = simps(sigma_z_val, z)
print("integral = {}".format(integral))
plt.plot(z,sigma_z_val, label = r'$\sigma_z$')
plt.xlabel="x"
plt.ylabel = "y"
plt.legend()
print("z = {} and sigma = {}".format(z,sigma_z_val))
plt.show()