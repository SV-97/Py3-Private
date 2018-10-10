from distutils.core import setup
from Cython.Build import cythonize
"""To build:
python3 setup.py build_ext --inplace
"""
setup(name="Calculate primes and store them in a file", ext_modules=cythonize("CalcPrimes.pyx"))