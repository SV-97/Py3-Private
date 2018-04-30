
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt

pi = np.pi
R = 14.1
L = 53.5e-3
C = 66e-6
f = np.linspace(0,20000,50000)
OMEGA = 2 * pi * f

@np.vectorize
def Y(omega):
    return np.complex(R/(R**2.0 + (omega*L)**2.0), (omega*C - ((omega*L)/(R**2.0 + (omega*L)**2.0))))

@np.vectorize
def Z(omega):
    return np.complex((R/(R**2.0+(omega*L)**2.0))/((R/(R**2.0+(omega*L)**2.0))**2.0+(omega*C - (omega*L)/(R**2.0+(omega*L)**2.0))**2.0) , (omega*C - (omega*L)/(R**2.0+(omega*L)**2.0))/((R/(R**2.0+(omega*L)**2.0))**2.0+(omega*C - (omega*L)/(R**2.0+(omega*L)**2.0))**2.0))

y = Y(OMEGA)
z = Z(OMEGA)

plt.subplot(2,1,1)
plt.plot(y.real,y.imag, linewidth = 2, label = "Y")
plt.ylabel("Imaginärteil")
plt.xlabel("Realteil")

plt.subplot(2,1,2)
plt.plot(z.real,z.imag, linewidth = 2, label = "Z")
plt.ylabel("Imaginärteil")
plt.xlabel("Realteil")

plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
plt.gcf().canvas.set_window_title("Ortskurven C || (RL)")
plt.legend()
plt.show()