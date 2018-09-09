import numpy as np
import sympy as sp

words = "SENDMOREMONEY"
words = set(words)
words = ", ".join(words)
S, Y, M, D, N, E, R, O = sp.symbols(words)

range_ = np.arange(0, 10)
mrange_ = np.arange(1, 10)

a = 10**0*(E + D) + 10**1*(N + R) + 10**2*(E + O) + 10**3*(S + M) - (10**0*Y + 10**1*E + 10**2*N + 10**3*O + 10**4*M)
# Equal to a = lambda S, E, R, D, M, O, N, Y: 10**0*(E + D) + 10**1*(N + R) + 10**2*(E + O) + 10**3*(S + M) - (10**0*Y + 10**1*E + 10**2*N + 10**3*O + 10**4*M)
print(a)
a = sp.lambdify([S, E, R, D, M, O, N, Y], a)
solutions = []
for i in range_:
    for j in range_:
        for k in range_:
            for l in range_:
                for m in mrange_:
                    for n in range_:
                        for o in range_:
                            for p in range_:
                                val = a(i, j, k, l, m, n, o, p)
                                if val == 0:
                                    solutions.append({"S":i, "E":j, "R":k, "D":l, "M":m, "O":n, "N":o, "Y":p})
                                    numbers = list(range_)
                                    try:
                                        for q in [i, j, k, l, m, n, o, p]:                                        
                                            numbers.pop(numbers.index(q))
                                    except ValueError:
                                        pass
                                    else:
                                        print("""
S = {}
E = {}
R = {}
D = {}
M = {}
O = {}
N = {}
Y = {}
                                        """.format(i, j, k, l, m, n, o, p))
print(solutions)