#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="pdf-unlocker",
    version="1.0",
    packages=find_packages(),
    scripts=['scripts/pdf-unlocker'],
    install_requires=[
        'pikepdf'
    ],
)
