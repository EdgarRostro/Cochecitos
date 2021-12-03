"""
Hello World app for running Python apps on Bluemix
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='cochecitos-city',
    version='1.0.0',
    description='Multiagent simulation of city traffic',
    url='https://github.com/EdgarRostro/Cochecitos',
    license='GNU'
)