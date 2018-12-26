from setuptools import setup, Extension
modul = Extension("chiffre", sources=["chiffre.c"])
setup(
    name="PyChiffre",
    version="1.0",
    description="Module for crazy encryption.",
    ext_modules=[modul]
)