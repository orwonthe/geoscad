#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from setuptools import setup, find_packages

# Package meta-data.
NAME = 'geoscad'
DESCRIPTION = 'Geometry Tools for SolidPython wrapping for OpenSCAD.'
AUTHOR = 'William Mills'
EMAIL = ''
URL = 'https://github.com/orwonthe/geoscad.git'
VERSION = '0.1.1'

REQUIRED = [
    'attrs==17.4.0',
    'euclid3==0.1',
    'more-itertools==4.1.0',
    'numpy==1.14.2',
    'pluggy==0.6.0',
    'prettytable==0.7.2',
    'py==1.5.3',
    'pypng==0.0.18',
    'pytest==3.5.0',
    'six==1.11.0',
    'solidpython==0.2.0',
]

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

our_packages = find_packages(include=['geoscad'])

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=our_packages,
    install_requires=REQUIRED,
    include_package_data=True,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    entry_points={
        'console_scripts': [
            # 'script_name = somefile.main:somefile_main',
        ]
    }
    # $ setup.py publish support.
    # cmdclass={
    #     'upload': UploadCommand,
    # },
)
