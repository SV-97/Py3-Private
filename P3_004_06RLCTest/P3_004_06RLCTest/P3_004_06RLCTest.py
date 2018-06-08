
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt

import timeit

pi = np.pi
R = 150
L = 100e-3
C = 10e-6
f = np.linspace(0,20e3,500000)
f = f[1:]
omega = 2 * pi * f

@np.vectorize
def CCE(c): #complex conjugated extension
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
def Z_RC_parallel_L(R,L,C,omega):
    Xc = 1/(omega*C)
    Xl = omega*L
    Bc = 1/Xc
    Bl = 1/Xl
    Z1 = 1j*Xl
    Z2 = R - 1j*Xc
    Y1 = CCE(Z1)
    Y2 = CCE(Z2)
    Yg = Y1+Y2
    Zg = CCE(Yg)
    return Zg

@np.vectorize
def Z_RL_parallel_C(R,L,C,omega):
    Xc = 1/(omega*C)
    Xl = omega*L
    Bc = 1/Xc
    Bl = 1/Xl
    Z1 = -1j*Xc
    Z2 = R + 1j*Xl
    Y1 = CCE(Z1)
    Y2 = CCE(Z2)
    Yg = Y1+Y2
    Zg = CCE(Yg)
    return Zg

z1 = Z_RC_parallel_L(R,L,C,omega)

height = 2
widths = 1

plt.subplot(height,widths,1)
plt.plot(z1.real,z1.imag, linewidth = 2, label = "RC || L")
plt.ylabel("Imaginärteil")
plt.xlabel("Realteil")
plt.legend()

omegar = 1/(np.sqrt(L*C))
fr = omegar/(2*pi)
z1r = Z_RC_parallel_L(R,L,C,omegar)
plt.annotate(r"$f_r$" + " = {:.2g}Hz".format(fr), xy=(z1r.real,z1r.imag))
plt.plot((z1.real[0],z1.real[len(z1)-1],z1r.real),(z1.imag[0],z1.imag[len(z1)-1],z1r.imag),"o")
plt.annotate("f = {:.2g}Hz".format(f[len(f)-1]), xy=(z1.real[len(z1)-1], z1.imag[len(z1)-1]))
plt.annotate("f = {:.2g}Hz".format(f[0]), xy=(z1.real[0], z1.imag[0]))

z2r = Z_RL_parallel_C(R,L,C,omegar)
z2 = Z_RL_parallel_C(R,L,C,omega)

plt.subplot(height,widths,2)
plt.plot(z2.real,z2.imag, linewidth = 2, label = "RL || C")
plt.ylabel("Imaginärteil")
plt.xlabel("Realteil")
plt.legend()

plt.annotate(r"$f_r$" + " = {:.2g}Hz".format(fr), xy=(z2r.real,z2r.imag))
plt.plot((z2.real[0],z2.real[len(z2)-1],z2r.real),(z2.imag[0],z2.imag[len(z2)-1],z2r.imag),"o")
plt.annotate("f = {:.2g}Hz".format(f[len(f)-1]), xy=(z2.real[len(z2)-1], z2.imag[len(z2)-1]))
plt.annotate("f = {:.2g}Hz".format(f[0]), xy=(z2.real[0], z2.imag[0]))

plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
plt.gcf().canvas.set_window_title("Ortskurven")
plt.show()