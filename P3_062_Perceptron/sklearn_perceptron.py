""" Perceptron that's kinda modeled after the sklearn implementation """

import random

import numpy as np

def heaviside(x):
    return 0 if x < 0 else 1


class Perceptron():
    def __init__(self, n_iterations):
        self.n_iterations = n_iterations
        self.errors = []
        self.random_gen = random.Random(1)
        self.w = []
        self.X = []
        self.y = []

    def fit(self, X, y):
        if len(X) != len(y):
            raise ValueError("Dimensions of X and y don't match up")

        self.w = np.array([self.random_gen.random() for _ in range(len(X[0]))])
        self.X = X
        self.y = y
        for _ in range(self.n_iterations):
            index = self.random_gen.randrange(0, len(y))
            x_ = self.X[index]
            y_ = self.y[index]
            y_hat = heaviside(self.w.dot(x_))
            error = y_ - y_hat
            self.errors.append(error)
            self.w += x_ * error
        

p = Perceptron(500)
X = [
    np.array([1, 0, 0]),
    np.array([1, 0, 1]),
    np.array([1, 1, 0]),
    np.array([1, 1, 1])]
y = np.array([0, 1, 1, 1])
p.fit(X, y)

print(p.w)