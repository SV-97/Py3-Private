from distutils.core import setup, Extension

module = Extension("testModule", sources=["testmodule.c"])
setup(name = "testmodule",
    version = "1.0",
    description = "Testing C and Python interoperability",
    author = "Stefan Volz",
    url = "https://github.com/SV-97",
    ext_modules = [module])