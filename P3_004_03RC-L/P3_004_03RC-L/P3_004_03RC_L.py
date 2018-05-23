
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt

import timeit

pi = np.pi
R = 10
L = 100e-3
C = 10e-6
f = np.linspace(0,20e9,500000)
f = f[1:]
OMEGA = 2 * pi * f

@np.vectorize
def Z(omega):
    Xc = 1/omega*C
    Xl = omega*L
    Z1 = np.complex(R,-Xc)
    Z2 = np.complex(0,Xl)
    Zg = (Z1*Z2)/(Z1+Z2)
    nenner = R**2+(Xl-Xc)**2
    #return np.complex((R*Xl*((Xl-Xc)+Xc))/nenner, (R**2*Xl-Xc*Xl*(Xl-Xc))/nenner)
    return Zg

z = Z(OMEGA)
y = 1/z

height = 2
widths = 1

plt.subplot(height,widths,1)
plt.plot(y.real,y.imag, linewidth = 2, label = "Y")
plt.ylabel("Imaginärteil")
plt.xlabel("Realteil")
plt.legend()

plt.subplot(height,widths,2)
plt.plot(z.real,z.imag, linewidth = 2, label = "Z")
#plt.semilogx(z.real, z.imag,linewidth = 2, label = "Z")
plt.ylabel("Imaginärteil")
plt.xlabel("Realteil")
plt.legend()

plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
plt.gcf().canvas.set_window_title("Ortskurven R||L")
plt.show()

"""
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import timeit

pi = np.pi
R = 50
L = 10e-6
C = 10e-6
f = np.linspace(0,20e6,50000)
f = f[1:]
OMEGA = 2 * pi * f

@np.vectorize
def Z(omega):
    Xc = 1/omega*C
    Xl = omega*L
    nenner = R**2-(Xl-Xc)**2
    return np.complex((R*Xc)/nenner, (Xl*(R**2-Xc*Xl-Xc**2))/nenner)

z = Z(OMEGA)
y = 1/z

height = 10
widths = 2

for i in range(0,height*2,2):
    R = (i+1)*100
    L = (i+1)*100e-3
    C = (i+1)*10e-6
    z = Z(OMEGA)
    y = 1/z

    plt.subplot(height,widths,1+i)
    plt.plot(y.real,y.imag, linewidth = 2, label = "Y"+str(i))

    plt.subplot(height,widths,2+i)
    plt.plot(z.real,z.imag, linewidth = 2, label = "Z"+str(i))

plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
plt.gcf().canvas.set_window_title("Ortskurven R||L")
plt.show()
"""