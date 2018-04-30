
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import cmath

pi = np.pi;
R = 14.1;
L = 53.5e-3;
C = 66e-6;
f = np.linspace(0,20000,500000);
OMEGA = 2 * pi * f;

def Y(omega):
    return np.complex(R/(R**2 + (omega*L)**2), (omega*C - ((omega*L)/(R**2 + (omega*L)**2))));

def Y_re(omega):
    return R/(R**2 + (omega*L)**2)

def Y_im(omega):
    return (omega*C - ((omega*L)/(R**2 + (omega*L)**2)))

f2 = np.vectorize(Y);
y = f2(OMEGA);
z = np.divide(y,1);
y = f2(OMEGA);
#z = 1/y;

if z.all() == y.all():
    print("1");
else:
    print("0");
    pass;
    
plt.plot(y.real,y.imag, linewidth = 2, linestyle = "dashed", label = "Y");
plt.plot(z.real,z.imag, linewidth = 2, label = "Z");
plt.show();

#plt.plot(Y_re(OMEGA),Y_im(OMEGA), linewidth = 2, linestyle = "dashed", label = "Y");