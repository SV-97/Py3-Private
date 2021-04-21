import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import seaborn as sns

from itertools import islice
from random import uniform
from collections import namedtuple
from collections.abc import MutableSequence
import statistics as stat
from itertools import count
from abc import abstractmethod, ABC


def take(it, n):
    return islice(it, n)


def chunk_iter(it, chunk_size):
    while True:
        yield take(it, chunk_size)


class RandomNumberGenerator(ABC):
    m = NotImplemented
    @abstractmethod
    def __call__(self, seed=0): pass

    @property
    def maximum(self):
        return self.m - 1


class RingBuffer(MutableSequence):
    def __init__(self, buffer: list):
        self._buffer = buffer
        self._size = len(buffer)

    def __getitem__(self, key):
        return self._buffer[key % self._size]

    def __setitem__(self, key, value):
        self._buffer[key % self._size] = value

    def __delitem__(self, key):
        del self._buffer[key % self._size]

    def __len__(self):
        return self._size

    def insert(self, key, value):
        self._buffer.insert(key, value)
        self._size = len(self._buffer)


class LinearCongruenceGenerator(RandomNumberGenerator):
    def __init__(self, a=742921174104182070222787289478667460939537,
                 c=277632652896428484830389019845849789540123, m=993191266486649425917817284380909955718231):
        self.a = a
        self.c = c
        self.m = m

    def __call__(self, seed=0):
        a = self.a
        c = self.c
        m = self.m
        xn = seed
        while True:
            xn = (a * xn + c) % m
            yield xn


class LEcuyerGenerator(RandomNumberGenerator):
    def __init__(self,
                 m=4294967087,
                 m_p=4294944443,
                 a_1=1403580,
                 a_2=810728,
                 a_1p=527612,
                 a_2p=1370589):
        self.m = m
        self.m_p = m_p
        self.a_1 = a_1
        self.a_2 = a_2
        self.a_1p = a_1p
        self.a_2p = a_2p

    def __call__(self, seed=0):
        m = self.m
        m_p = self.m_p
        a_1 = self.a_1
        a_2 = self.a_2
        a_1p = self.a_1p
        a_2p = self.a_2p
        # x_(n-3), x_(n-2), x_(n-1)
        x_n = RingBuffer([seed, seed, seed, None])
        x_np = RingBuffer([seed, seed, seed, None])
        for n in count(len(x_n) - 1):  # start ringbuffer at last element
            x_n[n] = (a_1 * x_n[n - 2] - a_2 * x_n[n-3]) % m
            x_np[n] = (a_1p * x_np[n-1] - a_2p * x_np[n-3]) % m_p
            x_npp = (x_n[n] - x_np[n]) % m
            if x_npp > 0:
                yield x_npp
            else:
                yield m


"""
class MersenneTwister(RandomNumberGenerator):
    def __call__(self, seed=0):
        n = 10  # size
        w = 5
        r = n-w
        u = np.array([1]*n)
        u[0:r+1] = 0
        ll = np.array([0]*n)
        ll[0:r+1] = 1
        a = np.array([0]*w) # genaue matrixwerte eintragen

        self.x = np.array([0]*n, dtype=np.uint) # hier iwie seed einarbeiten

        i = 0
        y = (x[i] & 0) | (x[(i+1) % n] & ll)
        x[i] = x[(i+m) % n] ^ (y >> 1)
"""


random_generator = LinearCongruenceGenerator()
#random_generator = LEcuyerGenerator()


def uniform_distribution(a=0, b=1, seed=0):
    m = random_generator.maximum
    for x in random_generator(seed):
        yield (b-a) * x / m + a


def exponential_distribution(alpha=3, seed=0):
    """Inversionsmethode"""
    for z in uniform_distribution(seed):
        yield - np.log(z) / alpha


def weibull_distribution(alpha=1, beta=1.5, seed=0):
    """Inversionsmethode"""
    for z in uniform_distribution(seed):
        yield (-np.log(z) / alpha)**(1/beta)


def normal_distribution(expected_value=0, std_dev=1, seed=0):
    """Approximation über zentralen Grenzwertsatz"""
    for z in chunk_iter(uniform_distribution(seed), 12):
        x = sum(z) - 6
        yield std_dev * x + expected_value


def rayleigh_distribution(sigma=1, seed=0):
    """Inversionsmethode"""
    for z in uniform_distribution(seed):
        if z < 0:
            yield 0
        else:
            yield np.sqrt(np.log(1 - z) * -2 * sigma**2)


def gumbel_distribution(beta=1, mu=0, seed=0):
    """Inversionsmethode"""
    for z in uniform_distribution(seed):
        yield -beta * np.log(np.log(1/z)) + mu


class SearchTree():
    """
    Todo: replace recursive structure with simple list and binary search on that
    """
    __slots__ = ("val", "left", "right", "len", "size")

    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self.len = 1 if val is not None else 0
        if left is not None:
            self.len += left.len
        if right is not None:
            self.len += right.len

    @staticmethod
    def from_lst(lst: list, already_sorted=False):
        if already_sorted:
            s = lst
        else:
            s = sorted(lst)
        if len(s) <= 2:
            if len(s) == 2:
                lv = s[0]
                rv = s[1]
                return SearchTree(lv, SearchTree(rv))
            elif len(s) == 1:
                return SearchTree(s[0])
            else:
                return SearchTree()
        else:
            pivot = len(s) // 2
            mid = s[pivot]
            l = s[:pivot]
            r = s[pivot+1:]
            left_sub = SearchTree.from_lst(l, True)
            right_sub = SearchTree.from_lst(r, True)
            t = SearchTree(mid, left_sub, right_sub)
            t.size = len(lst)
            return t

    def __len__(self):
        return self.len

    def __str__(self):
        if self.val is None:
            return "empty tree"
        if self.left is None and self.right is None:
            return f"leaf | {self.val}"
        return f"tree | val: {self.val}\n  left: {self.left}\n  right: {self.right}\n"

    def count_less_than(self, x):
        if self.val == x:
            return len(self.left) if self.left is not None else 0
        elif x < self.val:
            return self.left.count_less_than(x) if self.left is not None else 0
        else:  # x > self.val
            return (1  # this node
                    + (len(self.left) if self.left is not None else 0)  # left ones
                    + (self.right.count_less_than(x) if self.right is not None else 0))  # potentially right ones

    def max(self):
        if self.right is None:
            return self.val
        else:
            return self.right.max()

    def min(self):
        if self.left is None:
            return self.val
        else:
            return self.left.min()

    def find_least_upper_bound(self, x):
        if self.val >= x:
            if self.left is None:
                return self.val
            else:
                if self.left.max() < x:
                    return self.val
                else:
                    return self.left.find_least_upper_bound(x)
        else:
            if self.right is None:
                return None
            else:
                return self.right.find_least_upper_bound(x)

    def find_largest_lower_bound(self, x):
        if self.val <= x:
            if self.right is None:
                return self.val
            else:
                if self.right.min() > x:
                    return self.val
                else:
                    return self.right.find_largest_lower_bound(x)
        else:
            if self.left is None:
                return None
            else:
                return self.left.find_largest_lower_bound(x)

    def find_bounds(self, x):
        return (self.find_largest_lower_bound(x), self.find_least_upper_bound(x))


def approx_distribution_fn(distribution, n=10_000):
    sample = SearchTree.from_lst(list(take(distribution, n)))

    @np.vectorize
    def distribution_function(x):
        return sample.count_less_than(x) / sample.size
    distribution_function.sample = sample
    return distribution_function


def numerically_differentiate(f, h=1e-6):
    def df(x):
        return (f(x+h) - f(x-h)) / (2*h)
    return df


def approx_density_fn(distribution, n=10_000):
    # density_function = np.vectorize(numerically_differentiate(
    #    approx_distribution_fn(distribution, n)))
    d = approx_distribution_fn(distribution, n)
    sample = d.sample

    @np.vectorize
    def density_function(x):
        (lower, upper) = sample.find_bounds(x)
        if lower == upper:
            print(lower, x, upper)
        if None in (lower, upper):
            if lower is None:
                pass  # print("lower", x)
            if upper is None:
                pass  # rint("upper", x)
            return 0
        else:
            val = (d(upper) - d(lower)) / (upper - lower)
        if abs(val) < 10e-6:
            print(val)
            return val
    return density_function


def chunk(lst, chunk_size):
    return [lst[x:x+chunk_size] for x in range(0, len(lst), chunk_size)]


def smoothen(xs, ys, chunk_size):
    xs_buckets = list(map(np.mean, chunk(xs, chunk_size)))
    ys_buckets = []
    for c in chunk(ys, chunk_size):
        m = np.abs(c - np.mean(c)) <= 2*np.std(c)
        ys_buckets.append(np.mean(c[m]))
    f = interp1d(xs_buckets, ys_buckets, kind="cubic")
    xs_new = np.linspace(xs_buckets[0], xs_buckets[-1], len(xs))
    return xs_new, f(xs_new)


if __name__ == "__main__":
    N = 10_000

    Distribution = namedtuple(
        "Distribution", ("function", "label", "interval"))

    dists = [Distribution(*t) for t in (
        (uniform_distribution, r"$U[0,1]$", (-1, 2)),
        (exponential_distribution, r"$Exp(\lambda)$", (-0.5, 2.5)),
        (lambda: weibull_distribution(1, 1.5),
         r"Weibull, $\alpha=1, \beta=1.5$", (-0.5, 2.5)),
        (lambda: weibull_distribution(1, 5),
         r"Weibull, $\alpha=1, \beta=5$", (-0.5, 2.5)),
        (normal_distribution,
         r"$\mathcal{N} (0,1)$", (-4, 4)),
        (rayleigh_distribution,
         r"Rayleigh, $\sigma=1$", (-0.5, 4)),
        (gumbel_distribution,
         r"Gumbel, $\sigma=1, \mu=0$", (-2, 4)),)]
    n_dists = len(dists)
    n_buckets = 100
    cols = 3
    for i, dist in enumerate(dists):
        dist_fn = dist.function
        label = dist.function.__name__ if dist.label is None else dist.label

        ys = list(take(dist_fn(), N))
        xs = np.array(range(0, N))

        plt.subplot(n_dists, cols, 1+cols*i)
        plt.plot(ys, xs/N, ".")
        plt.plot(sorted(ys), xs/N, ".")
        sns.kdeplot(ys, bw=0.05)

        plt.subplot(n_dists, cols, 2+cols*i)
        # plt.title(label)
        xs = np.linspace(*dist.interval, N)
        ys = approx_distribution_fn(dist_fn())(xs)
        xs_dist_smooth, ys_dist_smooth = smoothen(xs, ys, N // n_buckets)
        # plt.plot(xs, ys)
        plt.plot(xs_dist_smooth, ys_dist_smooth)

        plt.subplot(n_dists, cols, 3+cols*i)
        #ys = approx_density_fn(dist_fn(), n=100_000)(xs)
        xs_dens_smooth, ys_dens_smooth = smoothen(
            xs_dist_smooth, np.gradient(ys_dist_smooth, xs_dist_smooth), N // n_buckets)
        # plt.plot(xs, ys)
        plt.plot(xs_dist_smooth, ys_dens_smooth, label=label)
        plt.legend()

        # plt.subplot(n_dists, cols, 4+cols*i)
        # plt.plot(xs_dist_smooth, np.gradient(ys_dist_smooth))
    plt.show()
