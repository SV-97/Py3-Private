""" Small exercise from a book about ANNs """

import matplotlib.pyplot as plt
import numpy as np


def heaviside(x):
    return 0 if x < 0 else 1


# [BIAS, left sensor(HIGH if obstacle), right sensor(HIGH if obstacle)]
X = np.array([ # input vectors - first element is bias neuron
    [1, 0, 0],
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 1]])

y = np.array([ # output vectors
    0,
    1,
    1,
    1])

def perceptron_eval(X, y):
    error_sum = 0
    w = np.array([-1, 1, 1])
    for i, x in enumerate(X):
        sum_i = np.dot(w, x)
        out_i = heaviside(sum_i)
        error_i = np.abs(out_i - y[i])
        error_sum += error_i
        print(f"Sensor Left: {x[1]}\nSensor Right: {x[2]}\nOutput: {y[i]}\nError: {error_i}\n\n")
    return error_sum

print(f"Overall error: {perceptron_eval(X,y)}")