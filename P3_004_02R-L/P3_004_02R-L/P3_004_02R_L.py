
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import timeit

pi = np.pi
R = 14.1
L = 53.5e-3
f = np.linspace(0,20000,50000)
f = f[1:]
OMEGA = 2 * pi * f

@np.vectorize
def Y(omega):
    return np.complex(1/R, -1/(omega*L))

@np.vectorize
def Z(omega):
    return np.complex((1/R)/(1/R**2+1/(omega*L)**2), (1/(omega*L))/(1/R**2+1/(omega*L)**2))

y = Y(OMEGA)
z = Z(OMEGA)
z2 = np.divide(1,y)
#z2 = 1/y

height = 3
widths = 1

plt.subplot(height,widths,1)
plt.plot(y.real,y.imag, linewidth = 2, label = "Y")
plt.ylabel("Imaginärteil")
plt.xlabel("Realteil")
plt.legend()

plt.subplot(height,widths,2)
plt.plot(z.real,z.imag, linewidth = 2, label = "Z")
plt.ylabel("Imaginärteil")
plt.xlabel("Realteil")
plt.legend()

plt.subplot(height,widths,3)
plt.plot(z2.real,z2.imag, linewidth = 2, label = "Z2")
plt.ylabel("Imaginärteil")
plt.xlabel("Realteil")
plt.legend()

plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
plt.gcf().canvas.set_window_title("Ortskurven R||L")
plt.show()