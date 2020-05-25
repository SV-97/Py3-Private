from itertools import zip_longest, dropwhile
from operator import add, sub
from functools import total_ordering, reduce
from typing import List, Union, Callable, Iterable

Number = Union[float, int, complex]


def zip_with(f: Callable, *iters: Iterable):
    return (f(*args) for args in zip(*iters))


def zip_with_longest(f: Callable, *iters: Iterable, ident=None):
    return (f(*args) for args in zip_longest(*iters, fillvalue=ident))


@total_ordering
class Poly():
    """ Polynomials
    The degree of the coefficient is the corresponding index into the list,
    so the leftmost coefficient is the constant.
    """

    __slots__ = ["coeffs"]

    def __init__(self, *coeffs: Number):
        coeffs_: Iterable[Number] = dropwhile(
            lambda c: c == 0, reversed(coeffs))
        self.coeffs = list(coeffs_)
        self.coeffs.reverse()

    def __iter__(self):
        return iter(self.coeffs)

    def scalar_mult(self, scalar: Number) -> "Poly":
        return Poly(*map(lambda x: x*scalar, self.coeffs))

    def __add__(self, other: "Poly") -> "Poly":
        return Poly(*zip_with_longest(add, self.coeffs, other.coeffs, ident=0))

    def __sub__(self, other: "Poly") -> "Poly":
        return Poly(*zip_with_longest(sub, self.coeffs, other.coeffs, ident=0))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Poly):
            return NotImplemented
        return self.coeffs == other.coeffs

    def __lt__(self, other: "Poly") -> bool:
        return len(self.coeffs) < len(other.coeffs)

    def __rshift__(self, n: int) -> "Poly":
        """
        Increase degree of self by n - filling in the lower degree terms with zeros
        """
        new_coeffs: List[Number] = [0] * n
        new_coeffs.extend(self.coeffs)
        self.coeffs = new_coeffs
        return self

    def __mul__(self, other: "Poly") -> "Poly":
        aa = min(self, other)
        bb = max(self, other)
        coeffs_new = reduce(add, (bb.scalar_mult(
            a) >> deg for deg, a in enumerate(aa)))
        return Poly(*coeffs_new)

    def __call__(self, x: Number) -> Number:
        def horner(old, new):
            return old * x + new
        return reduce(horner, reversed(self.coeffs))

    def __str__(self):
        strs = (f"{c}∙x^{deg}" for deg, c in enumerate(self.coeffs))
        return " + ".join(strs)

    def __repr__(self):
        return f"Poly({self.coeffs})"


print(Poly(1, 2, 3) * Poly(4, 5, 6))
print(Poly(0, 2, 4)(69))
