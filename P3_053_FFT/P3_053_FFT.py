from math import e, floor, log2, pi, sin
from time import time

import matplotlib.pyplot as plt


def fft(f):
    n = len(f)
    if n == 1:
        return f
    else:
        half_n = n//2
        g = fft(f[::2])
        u = fft(f[1::2])
        c_k_1 = [g[k] + u[k] * e**(-2 * pi * 1j * k / n) for k in range(half_n)]
        c_k_2 = [g[k] - u[k] * e**(-2 * pi * 1j * k / n) for k in range(half_n)]
        c_k_1.extend(c_k_2)
        return c_k_1


def linspace(start, stop, n):
    n = int(n)
    step_size = (stop - start)/n
    return [start + step_size * i for i in range(0, n)]


def arange(start, step_size, n=1):
    n = int(n)
    return [start + step_size * i for i in range(0, n)]


def padded_fft(f):
    if log2(len(f)) % 1: # if the length of n is no power of 2
        next_power_of_2 = log2(len(f)) - log2(len(f)) % 1 + 1
        padding = [0 for i in range(0, int(2**next_power_of_2) - len(f))]
    padded_f = f[:] + padding
    return fft(padded_f)[:len(f)]


def fft_freq(len_t, sample_rate):
    return [1/sample_rate * i/len_t - 1/(sample_rate * len_t) for i in range(len_t//2)]


def rectwave(peak, frequency, time, phase, reference): # adapted from iphipy
    T = 1/frequency
    exp = floor(2*(time-phase)/T)
    return peak * pow(-1, exp) + reference


def approx_rectwave(peak, frequency, time, phase, reference, terms):
    terms = [1/n * peak * sin(2 * pi * frequency * time * n + phase) for n in range(1, terms*2 + 1, 2)]
    return 4/pi * sum(terms) + reference


values = 2**15
min_value = 0
max_value = 5
sample_rate = values / (max_value - min_value)

t = linspace(min_value, max_value, values)

##
wave = [rectwave(1, 1, x, 0, 0) for x in t]
t1 = time()
wave_fft = fft(wave)[:len(t)//2]
t2 = time()
print(t2-t1)
wave_fft = [abs(x) for x in wave_fft]

wave_fft_freq = fft_freq(len(wave), 1/sample_rate)

plt.subplot(2, 2, 1)
plt.plot(t, wave, label="Square-wave")
plt.legend()
plt.subplot(2, 2, 2)
plt.semilogx(wave_fft_freq, wave_fft, label="FFT")
plt.legend()

##
wave = [approx_rectwave(1, 1, x, 0, 0, 10) for x in t]
wave_fft = fft(wave)[:len(t)//2]
wave_fft = [abs(x) for x in wave_fft]

wave_fft_freq = fft_freq(len(wave), 1/sample_rate)

plt.subplot(2, 2, 3)
plt.plot(t, wave, label="Approximated square-wave")
plt.legend()
plt.subplot(2, 2, 4)
plt.semilogx(wave_fft_freq, wave_fft, label="FFT")
plt.legend()


plt.show()