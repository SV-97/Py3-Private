from math import exp, log, pi, sin, tan
from time import time


def function(a):
    return sin(a)


def composite_simpsons(f, a, b, n):
    step_size = (b - a) / n
    integral = 0
    for k in range(n):
        x_k = a + k * step_size;
        x_k1 = a + (k + 1) * step_size;

        simpson = step_size / 6 * (f(x_k) + 4 * f((x_k + x_k1) / 2 ) + f(x_k1))
        integral += simpson
    return integral

t1 = time()
integral_of_function = composite_simpsons(function, 0, 2*pi, 100000)
t2 = time()
print(f"Integration took {t2-t1} seconds")
print(f"F approx: {integral_of_function}")