#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
)
