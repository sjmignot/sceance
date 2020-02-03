# -*- coding: utf-8 -*-

'''
setup.py file for sceance
'''

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys

if sys.version_info[:3] < (3, 0, 0):
    print("Requires Python 3 to run.")
    sys.exit(1)

with open('README.rst') as f:
    README = f.read()

with open('LICENSE') as f:
    LICENSE = f.read()

setup(
    name='sample',
    version='0.1.0',
    description='Uses a watchlist and favorite theaters to suggest film screenings.',
    long_description=README,
    author='Samuel Mignot',
    author_email='sjmignot@gmail.com',
    url='https://github.com/sjmignot/sceance',
    license=LICENSE,
    entry_points={"console_scripts": ["sceance= sceance.sceance:main"]},
)
