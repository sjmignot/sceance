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

with open(path.join(this_directory, 'LICENSE', encoding='utf-8') as f:
    LICENSE = f.read()

setup(
    name='sample',
    version='0.1.0',
    description='Uses a watchlist and favorite theaters to suggest film screenings.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Samuel Mignot',
    author_email='sjmignot@gmail.com',
    url='https://github.com/sjmignot/sceance',
    download_url='https://github.com/sjmignot/sceance/archive/v_01.tar.gz',
    keywords = ['movie theater', 'showtimes', 'selenium', 'movies', 'film'],
    install_requires=[
        'requests>2'
        'google_api_python_client>1'
        'google_auth_oauthlib'
        'pandas'
        'protobuf>3'
        'selenium>3'
        'webdriver_manager>2'
    ],
    license=LICENSE,
    entry_points={"console_scripts": ["sceance= sceance.sceance:main"]},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
