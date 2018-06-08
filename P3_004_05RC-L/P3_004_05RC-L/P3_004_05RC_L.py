
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt

import timeit

pi = np.pi
R1 = 180
R2 = 150
L = 10e-3
C = 10e-6
f = np.linspace(0,20e3,500000)
f = f[1:]
omega = 2 * pi * f

@np.vectorize
def CCE(c): #complex conjugated extension - equal to 1/c
    O = np.float64(0)
    if c.imag == O and c.real == O:
        return O
    elif c.imag == O:
        return 1/c.real
    elif c.real == O:
        return -1j/c.imag
    else:
        return (c.real - 1j*c.imag)/(c.real**2 + c.imag**2)

@np.vectorize
def Y():
    Xc = 1/(omega*C)
    Xl = omega*L
    Yg = (R1+1j*Xc)/(R1**2+Xc**2)+(R2-1j*Xl)/(R2**2+Xl**2)
    return Yg

y = Y()
z = CCE(y)

height = 2
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

plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
plt.gcf().canvas.set_window_title("Ortskurven RC||L")
plt.show()