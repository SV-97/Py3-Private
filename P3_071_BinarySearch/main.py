from abc import ABC, abstractmethod
from collections import namedtuple
from collections.abc import Sequence


class Slice(Sequence):
    __slots__ = ("start", "len", "stop", "parent")

    def __init__(self, parent, start=0, length=None):
        if start >= len(parent):
            raise ValueError("Value of start too big", start)
        self.start = start
        self.len = length if length is not None else len(parent)
        self.stop = self.start + self.len
        self.parent = parent

    def __getitem__(self, key):
        if isinstance(key, slice):  # doesn't handle step != 1
            key_start = key.start if key.start is not None else 0
            start = self.start + key_start
            length = max(min(self.len - key_start if key.stop is None else
                             key.stop + key_start, self.len), 0)
            return Slice(self.parent, start, length)
        else:
            if key >= 0:
                return self.parent[self.start + key]
            else:
                return self.parent[self.stop + key]

    def __len__(self):
        return self.len

    def __str__(self):
        return f"&{self.parent[self.start:self.stop]}"

    def __repr__(self):
        return f"Slice(start={self.start}, length={self.len}) = {str(self)}"


def split(segment):
    return (segment[:len(segment)//2], segment[len(segment)//2:])


class Segment(ABC):
    def __init__(self, parent):
        self.parent = parent

    @abstractmethod
    def choose(self): pass


class LeftSegment(Segment):
    __slots__ = ("parent",)
    def choose(self): return self.parent.choose_left()

    def __contains__(self, value):
        return value <= self.parent.left[-1]


class RightSegment(Segment):
    __slots__ = ("parent",)
    def choose(self): return self.parent.choose_right()


Middle = namedtuple("Middle", ["value", "idx"])


class BinaryPartitions():
    __slots__ = ("left", "right", "level", "idx_offset")

    def __init__(self, data):
        # (self.left, self.right) = split(sorted(data))
        (self.left, self.right) = split(data)
        self.level = 0
        self.idx_offset = 0

    def __iter__(self):
        return self

    def __next__(self):
        mid = Middle(self.right[0], self.idx_offset + len(self.left))
        return (LeftSegment(self), mid, RightSegment(self))

    def choose_left(self):
        (self.left, self.right) = split(self.left)

    def choose_right(self):
        self.idx_offset += len(self.left)
        (self.left, self.right) = split(self.right)


def binary_search_1(data, value):
    for (left, middle, right) in BinaryPartitions(data):
        if value == middle.value:
            return middle.idx
        elif value in left:
            left.choose()
        else:
            right.choose()


def binary_search_2(data, value):
    hi = len(data) - 1
    lo = 0
    # data = sorted(data)
    while lo <= hi:
        mid = (lo+hi) // 2
        if data[mid] > value:
            hi = mid - 1
        elif data[mid] < value:
            lo = mid + 1
        else:
            return mid
    return hi


if __name__ == "__main__":
    from timeit import timeit
    N = 1000

    setup = """
from main import binary_search_1, binary_search_2, Slice
from random import choice, seed, sample
seed(1)
data = sorted(sample(list(range(1,1_000_000)), 100_000))
val = choice(data)
    """
    run_1 = "binary_search_1(data, val)"
    run_2 = "binary_search_2(data, val)"
    run_3 = "binary_search_1(Slice(data), val)"

    t2 = timeit(run_2, setup=setup, number=N)
    print("straight up: ", t2)
    t1 = timeit(run_1, setup=setup, number=N)
    print("fancy: ", t1)
    t3 = timeit(run_3, setup=setup, number=N)
    print("optimized fancy: ", t3)

    print("fancy takes ", t1 / t2, " times as long")
    print("optimized fancy takes ", t1 / t3, " times as long")
    # print(binary_search([1, 2, 3, 4, 5, 6, 7, 8, 9], 7))
