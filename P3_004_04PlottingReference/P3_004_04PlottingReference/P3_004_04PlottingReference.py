
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt

pi = np.pi # added simple pi just for comfort
R = 14.1
L = 53.5e-3 # = 55,5 * 10^(-3)
C = 66e-6
f = np.linspace(0,20000,50000) # 50k values from 0 to 20k
OMEGA = 2 * pi * f

@np.vectorize #decorator to make the following function be able to work with vectors
def Y(omega):
    return np.complex(R/(R**2.0 + (omega*L)**2.0), (omega*C - ((omega*L)/(R**2.0 + (omega*L)**2.0))))

@np.vectorize
def Z(omega):
    return np.complex((R/(R**2.0+(omega*L)**2.0))/((R/(R**2.0+(omega*L)**2.0))**2.0+(omega*C - (omega*L)/(R**2.0+(omega*L)**2.0))**2.0) , (omega*C - (omega*L)/(R**2.0+(omega*L)**2.0))/((R/(R**2.0+(omega*L)**2.0))**2.0+(omega*C - (omega*L)/(R**2.0+(omega*L)**2.0))**2.0))

y = Y(OMEGA)
z = Z(OMEGA)

plt.subplot(2,1,1) # Split the figure into a grid that's 1 field wide and 2 fields high and select the first one(left to right; up to down)
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
plt.gcf().canvas.set_window_title("Ortskurven C || (RL)") # name of the window the plot is in

####################################################################################################################

plt.figure() #Add new Output window that is shown parallel to the other one

R1 = 10*pi
R2 = 20*pi
L1 = 5e-3
L2 = 5e-3
Ue = 24
f = np.linspace(0,500000,50000)
f = f[1:] # slice all the elements from 1 to the last from f and assign it to f; equal to f = np.delete(f,0)
omega = 2 * pi * f

@np.vectorize
def Ua(omega):
    U2 = Ue/(np.sqrt(1+((R1/(omega*L1))**2 )))
    return U2/(np.sqrt(1+(((omega*L2)/R2)**2)))

@np.vectorize
def Spannungsverstaerkung(U1,U2):
    return 20*np.log10(U2/U1)

@np.vectorize
def Phasenverschiebung(omega):
    XL1 = omega*L1
    XL2 = omega*L2
    return np.arctan(-(XL1 * (R2**2 - XL1*XL2 + XL2**2)) / (R1 * (R2**2 + (XL1 + XL2)**2 ) + R2 * XL1**2))

ua = Ua(omega)
a = Spannungsverstaerkung(Ue, ua)
phi = Phasenverschiebung(omega)

plt.subplot(3,1,1)
#plt.plot(f,ua, linewidth = 2, label = "Ua")
plt.semilogx(f,ua,label="Ua") # plot with semilogarithmic scale
plt.ylabel("Spannung in V")
plt.xlabel("Frequenz in Hz")
plt.grid() # show x-y grid in the plot
plt.legend()

plt.subplot(3,1,2)
#plt.plot(f, a, linewidth = 2, label = "a")
plt.semilogx(f,a,label="a", color = "green")
plt.ylabel("Spannungsdaempfung in dB")
plt.xlabel("Frequenz in Hz")
plt.grid()
plt.legend()

plt.subplot(3,1,3)
#plt.plot(f, phi, linewidth = 2, label = "phi")
plt.semilogx(f,phi,label="phi", color = "red")
plt.ylabel("Winkel in rad")
plt.xlabel("Frequenz in Hz")
plt.grid()
plt.legend()

plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
plt.gcf().canvas.set_window_title("Kenndaten RLRL-Bandpass Filter")

plt.show()