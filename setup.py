# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys

if sys.version_info[:3] < (3, 0, 0):
    print("Requires Python 3 to run.")
    sys.exit(1)

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sample',
    version='0.1.0',
    description='Uses a watchlist and favorite theaters to suggest film screenings',
    long_description=readme,
    author='Samuel Mignot',
    author_email='sjmignot@gmail.com',
    url='https://github.com/sjmignot/film-to-cal',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
    entry_points={"console_scripts": ["film_to_calc = film_to_calc.film_to_calc:main"]},
)

