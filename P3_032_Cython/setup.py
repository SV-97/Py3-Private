from distutils.core import setup
from Cython.Build import cythonize
"""To build:
python3 setup.py build_ext --inplace
"""
setup(name="Hello World App", ext_modules=cythonize("P3_032_Cython.pyx"))