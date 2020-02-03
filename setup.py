# -*- coding: utf-8 -*-

'''
setup.py file for sceance
'''

from setuptools import setup, Extension
import sys

if sys.version_info[:3] < (3, 0, 0):
    print("Requires Python 3 to run.")
    sys.exit(1)

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='sceance',
    author='Samuel Mignot',
    author_email='sjmignot@gmail.com',
    version='0.1.5.9',
    description='Uses a watchlist and favorite theaters to suggest film screenings.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sjmignot/sceance',
    download_url='https://github.com/sjmignot/sceance/archive/v_01.tar.gz',
    packages=['sceance'],
    package_dir={'sceance': 'sceance'},
    package_data={'sceance': ['data/*.txt']},
    keywords = ['movie theater', 'showtimes', 'selenium', 'movies', 'film'],
    install_requires=[
        'requests>2',
        'google_api_python_client>1',
        'google_auth_oauthlib',
        'pandas',
        'protobuf>3',
        'selenium>3',
        'webdriver_manager>2',
    ],
    liscence="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ]
)
