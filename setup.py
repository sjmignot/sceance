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

from os import path
this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sample',
    version='0.1.0',
    description='Uses a watchlist and favorite theaters to suggest film screenings.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Samuel Mignot',
    author_email='sjmignot@gmail.com',
    url='https://github.com/sjmignot/sceance',
    license=LICENSE,
    entry_points={"console_scripts": ["sceance= sceance.sceance:main"]},
)
