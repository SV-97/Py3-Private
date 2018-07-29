
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt

pi = np.pi
R = 100
L = 10e-3
C = 100e-6
f = np.linspace(0,200000,500000)
f = f[1:]
#f = np.append(np.linspace(0,f[1], 50000)[1:],f)
omega = 2 * pi * f

@np.vectorize
def Y(equiv = False):
    if equiv:
        XL = omega*L
        XC = 1/(omega*C)
        Z1 = R + 1j*XL
        Z2 = R - 1j*XC
        Y  = 1/Z1 + 1/Z2
    else:
        Lp = (R**2+(omega*L)**2)/(omega**2*L)
        R1p = (R**2+(omega*L)**2)/(R)
        R2p = (R**2+(1/(omega*C))**2)/(R)
        Cp = (1/(omega**2*C))/(R**2+(1/(omega*C))**2)
        XLp = omega*Lp
        XCp = 1/(omega*Cp)
        Y = 1/R1p + 1/R2p + 1j*(1/XCp - 1/XLp)
    return Y

@np.vectorize
def Z():
    XL = omega*L
    XC = 1/(omega*C)
    Z1 = R + 1j*XL
    Z2 = R - 1j*XC
    Z  = 1/(1/Z1 + 1/Z2)
    return Z


y = Y()
z = Z()
z = (y.real-1j*y.imag)/(y.real**2+y.imag**2) #alternative formula 

plt.subplot(2,1,1)
plt.plot(y.real,y.imag, linewidth = 2, label = "Y")
plt.ylabel("Imaginärteil") # label the y axis
plt.xlabel("Realteil") # label the x axis
plt.legend() # show a small window with the label assigned in plot + the colour of the line

plt.subplot(2,1,2)
plt.plot(z.real,z.imag, linewidth = 2, label = "Z")
plt.ylabel("Imaginärteil")
plt.xlabel("Realteil")
plt.legend()

plt.subplots_adjust(wspace = 0.3, hspace = 0.3) # spacing between subplots/window
plt.gcf().canvas.set_window_title("Ortskurven (RC) || (RL)") # name of the window the plot is in

plt.figure()

plt.subplot(3,1,1)
plt.semilogx(f,y.imag, linewidth = 2, label = "[Im]Y")
plt.ylabel("Imaginärteil")
plt.xlabel("f")
plt.legend()
plt.grid()

plt.subplot(3,1,2)
plt.semilogx(f,y.real, linewidth = 2, label = "[Re]Y")
plt.ylabel("Realteil")
plt.xlabel("f")
plt.legend()
plt.grid()

plt.subplot(3,1,3)
plt.semilogx(f,abs(y), linewidth = 2, label = "|Y|")
plt.ylabel("Betrag")
plt.xlabel("f")
plt.legend()
plt.grid()

plt.subplots_adjust(wspace = 0.3, hspace = 0.3) # spacing between subplots/window
plt.gcf().canvas.set_window_title("Admitanz (RC) || (RL)") # name of the window the plot is in

plt.figure()

plt.subplot(3,1,1)
plt.semilogx(f,z.imag, linewidth = 2, label = "[Im]Z")
plt.ylabel("Imaginärteil")
plt.xlabel("f")
plt.legend()
plt.grid()

plt.subplot(3,1,2)
plt.semilogx(f,z.real, linewidth = 2, label = "[Re]Z")
plt.ylabel("Realteil")
plt.xlabel("f")
plt.legend()
plt.grid()

plt.subplot(3,1,3)
plt.semilogx(f,abs(z), linewidth = 2, label = "|Z|")
plt.ylabel("Betrag")
plt.xlabel("f")
plt.legend()
plt.grid()

plt.subplots_adjust(wspace = 0.3, hspace = 0.3) # spacing between subplots/window
plt.gcf().canvas.set_window_title("Impedanz (RC) || (RL)") # name of the window the plot is in

max = np.amax(abs(y))
print (f[np.where(abs(y) == max )[0][0]-1:np.where(abs(y) == max )[0][0]+2])

plt.show()
