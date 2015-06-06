#! /usr/bin/env python
"""
Author: Dario ML
Program: SETUP.PY
Date: Saturday, June 06, 2014
Description: Setup and install TD algorithms.
"""

from distutils.core import setup

setup(name='paer',
    version='0.01',
    description='Python Address Event Representation (AER) Library',
    author="Dario Magliocchetti-Lombi",
    author_email="darioml1911@gmail.com",
    package_dir={"paer" : "src"},
    packages=["paer"],
    install_requires=[
        'numpy',
        'matplotlib'
    ])
