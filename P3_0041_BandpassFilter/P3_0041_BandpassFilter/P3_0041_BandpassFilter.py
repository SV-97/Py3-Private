
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import decimal

pi = decimal.Decimal(np.pi)
pi = np.pi

R1 = 10*pi
R2 = 20*pi
L1 = 5e-3
L2 = 5e-3
Ue = 24
f = np.linspace(0,500000,num=50000)
if 0 in f:
    f = np.delete(f,0)
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

plt.subplot(1,1,1)
#plt.plot(f,ua, linewidth = 2, label = "Ua")
plt.semilogx(f,ua,label="Ua")
plt.ylabel("Spannung in V")
plt.xlabel("Frequenz in Hz")
plt.grid()
plt.legend()

plt.show()
plt.subplot(1,1,1)
#plt.plot(f, a, linewidth = 2, label = "a")
plt.semilogx(f,a,label="a", color = "green")
plt.ylabel("Spannungsdaempfung in dB")
plt.xlabel("Frequenz in Hz")
plt.grid()
plt.legend()
plt.show()

plt.subplot(1,1,1)
#plt.plot(f, phi, linewidth = 2, label = "phi")
plt.semilogx(f,phi,label="phi", color = "red")
plt.ylabel("Winkel in rad")
plt.xlabel("Frequenz in Hz")
plt.grid()
plt.legend()

plt.subplots_adjust(wspace = 0.3, hspace = 0.3)
plt.gcf().canvas.set_window_title("Kenndaten RLRL-Bandpass Filter")

plt.show()