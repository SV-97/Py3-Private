import matplotlib.pyplot as plt
from cmath import polar, pi, exp, sqrt
from typing import List


def roots(z: complex, n: int) -> List[complex]:
    roots = [z ** (1/n)]
    angle = exp(2j * pi / n)
    for _ in range(1, n+1):
        roots.append(roots[-1] * angle)
    return roots


def plot_polar(zs: List[complex]):
    polars = [polar(z) for z in zs]
    rs, args = zip(*polars)

    plt.polar(args, rs, "o")


plot_polar(roots(-1+sqrt(3)*1j, 3))
plt.show()
