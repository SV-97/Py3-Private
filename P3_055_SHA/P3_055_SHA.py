from functools import wraps
from math import ceil, floor, log2
from operator import and_, floordiv, lshift, or_, rshift, sub, xor
from time import time

import matplotlib.pyplot as plt


class BidirectionalDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        super().__setitem__(value, key)

    def __delitem__(self, key):
        super().__delitem__(self[key])
        super().__delitem__(key)


def bidirectional_cache(function):
    """Function decorator for caching
    For functions where f(f(x)) == x is True
    Requires hashable args and doesn't support kwargs
    """
    cache = BidirectionalDict()
    @wraps(function)
    def wrapped(*args):
        if hash(args) not in cache:
            print(f"Added {hash(args)} to cache")
            cache[hash(args)] = function(*args)
        return cache[hash(args)]
    return wrapped


class Bitstring():
    def __init__(self, n=None, data=None):
        """Series of bits to handle loweh-level binary data
        Args:
            data (int): positive integer that represents your data
            n (int): target length of your bitstring
        """
        if n is None:
            if data is None:
                raise ValueError("You can't construct an empty Bitstring without specifying its length")
            n = next_power_of_two(data)
        elif data is None:
            data = 0

        self.n = n
        self._raw_data = data
        self._str = None
    
    @staticmethod
    @bidirectional_cache
    def _str_to_int(val):
        return sum((2**i if val[i] else 0 for i in range(len(self.val))))

    @staticmethod
    def bits_needed(x):
        try:
            return floor(log2(x)) + 1
        except ValueError:
            return 1

    def __int__(self):
        return self._raw_data

    def __float__(self):
        return float(self._raw_data)

    def __str__(self):
        data = bin(abs(self._raw_data))[2:]
        if len(data) > self.n:
            raise ValueError(f"Can't fit data into {self.n}-bit integer")
        while len(data) != self.n:
            data = "0" + data
        self._str = data
        return data

    def __repr__(self):
        return f"{self.__class__} at {id(self)}: {self}"

    def _int_op(self, other, function):
        return self.__class__(self.n, function(int(self), int(other)))

    def __add__(self, other):
        return self._int_op(other, add)

    def __sub__(self, other):
        return self._int_op(other, sub)

    def __mul__(self, other):
        return self._int_op(other, mul)

    def __div__(self, other):
        return float(self) / float(other)

    def __floordiv__(self, other):
        return self._int_op(other, floordiv)

    def __lshift__(self, other):
        self.n += 1
        return self._int_op(other, lshift)
    
    def __rshift__(self, other):
        self.n -= 1
        return self._int_op(other, rshift)

    def __xor__(self, other):
        return self._int_op(other, xor)

    def __and__(self, other):
        return self._int_op(other, and_)
    
    def __or__(self, other):
        return self._int_op(other, or_)

    def __invert__(self):
        str_ = str(self)
        str_ = "".join(("0" if x == "1" else "1" for i in str_))
        return self.__class__(self.n, self._str_to_int(str_))

    def ror(self, n):
        """Rotate right by n places
        Args:
            n (int): number of places to rotate by
        """
        str_ = str(self)
        return self.__class__(self._str_to_int(str_[len(str_) - n:][::-1] + str_[:len(str_) - n]))

    def rol(self, n):
        """Rotate left by n places
        Args:
            n (int): number of places to rotate by
        """
        str_ = str(self)
        return self.__class__(self._str_to_int(str_[:n] + str_[n:][::-1]))

    def __len__(self):
        return self.n
    
    def __getitem__(self, key):
        str_ = str(self)
        return 

    def __hash__(self):
        return hash(self._raw_data)


def next_power_of_two(x):
    if x == 0:
        return 2
    return 2**ceil(log2(x))


def sha_256(message):

    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h4 = 0x510e527f
    h5 = 0x9b05688c
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19

    k = (
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        )
    
    block_size = 512

    
    message = int.from_bytes(message, "big")
    L = Bitstring.bits_needed(message)

    if Bitstring.bits_needed(L) > 64:
        raise ValueError("Message is too big - lengths in bits exceeds 64-bit maximum")
    
    bits_to_pad = int(block_size * (ceil((L+1+64) / block_size) - (L+1+64)/block_size))

    total_size = L + 64 + 1 + bits_to_pad
    message = Bitstring(total_size, data=message)
    message_to_process = (((message << 1) | 1) << bits_to_pad + 64) | L
    print(message_to_process)
    message_bin = bin(message_to_process)[2:]
    while len(message_bin) % block_size: # add automatically truncated leading zeros
        message_bin = "0" + message_bin
    
    chunks = [message_bin[i*block_size:(i+1)*block_size] for i in range(len(message_bin) // 512)]
    for chunk in chunks:
        w = [chunk[i*32:(i+1)*32] for i in range(block_size // 32)] # message_schedule_arr
        w += [0 for i in range(64 - 32)]
        for i in range(16, 64):
            so = (w[i - 15] ) ^ () ^ ()
"""
message = b""
sha_256(message)"""

class A():
    N = 1
    def __init__(self, n):
        self.n = n

    def __hash__(self):
        return hash(self.n)

    def __add__(self, other):
        return self.__class__(int(self) + int(other))

    def __int__(self):
        return self.n

    @bidirectional_cache
    def test(self):
        return f"n = {self.n}"

    @staticmethod
    @bidirectional_cache
    def test_static(a, b):
        return a + b
    
    @classmethod
    @bidirectional_cache
    def test_class(cls, b):
        return cls.N + b


a = A(5)
print(a.test())
a = a + 2
print(a.test())
print(a.test())
b = A(5)
print(b.test())

print(a.test_static(1,2))
print(b.test_static(1,2))
print(a.test_static(1,2))

print(a.test_class(4))
print(b.test_class(4))
print(A.test_class(4))
print(A.test_class(5))