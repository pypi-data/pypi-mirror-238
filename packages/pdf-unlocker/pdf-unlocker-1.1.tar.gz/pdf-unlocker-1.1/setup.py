#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setup(
  name="pdf-unlocker",
  version="1.1",
  packages=find_packages(),
  scripts=['scripts/pdf-unlocker'],
  install_requires=[
    'pikepdf'
  ],
  long_description=long_description,
  long_description_content_type="text/markdown"
)
