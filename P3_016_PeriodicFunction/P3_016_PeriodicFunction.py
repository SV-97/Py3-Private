import numpy as np
import matplotlib.pyplot as plt
"""
spitze = 325
frequenz = 50
verschiebung = 1*np.pi
DC = 20
step = 1/(4*frequenz)
steps = [i/(4*frequenz) for i in np.linspace(1,4,4)]
x0 = np.linspace(0, 2/frequenz, 20e3)
x1 = np.linspace(0,steps[0])
x2 = np.linspace(steps[0], steps[2])
x3 = np.linspace(steps[2], steps[3])
steigung = 4*spitze*frequenz

f0 = lambda x: spitze*np.sin(2*np.pi*frequenz*x+verschiebung)+DC # sinuswelle referenz
f1 = lambda x: steigung*(x)+DC # erster abschnitt
f2 = lambda x: -steigung*(x-1/(2*frequenz))+DC # zweiter abschnitt
f3 = lambda x: steigung*(x-1/(frequenz))+DC # dritter abschnitt
f4 = lambda x: 0 # baseline
f0 = np.vectorize(f0)
f1 = np.vectorize(f1)
f2 = np.vectorize(f2)
f3 = np.vectorize(f3)
f4 = np.vectorize(f4)
@np.vectorize
def tri(x):
    xv = x+verschiebung*steps[3]/(2*np.pi)
    if xv > steps[3]:
        xv -= xv//steps[3]*steps[3]
    if  0 <= xv and xv <= steps[0]:
        return f1(xv)
    elif steps[0] < xv and xv <= steps[2]:
        return f2(xv)
    elif steps[2] < xv and xv <= steps[3]:
        return f3(xv)
    
y0 = f0(x0)
#y1 = f1(x1)
#y2 = f2(x2)
#y3 = f3(x3)
y4 = f4(x0)
y5 = tri(x0)
plt.plot(x0,y0)
#plt.plot(x1,y1)
#plt.plot(x2,y2)
#plt.plot(x3,y3)
plt.plot(x0,y5)
plt.plot(x0,y4, color = "k")
plt.plot([0,0],[0,1], color = "k")
plt.grid()
plt.show()
"""

a = 5
base_f  = 1e-20
T = 1/base_f
f = base_f/(2*np.pi)
omega = 2*np.pi*f
t = np.linspace(0,T,500e3)
shift = 0
@np.vectorize
def funktion(x):
    x = x-T/4-shift*T/(2*np.pi)
    betrag = max((1-((2*base_f*x)%2)), -1)
    return 2*a*abs(betrag)-a
y = funktion(t)
@np.vectorize
def sine(x):
    return a*np.sin(2*np.pi*base_f*x+shift)
plt.plot(t, sine(t))
plt.plot(t,y)
plt.show()