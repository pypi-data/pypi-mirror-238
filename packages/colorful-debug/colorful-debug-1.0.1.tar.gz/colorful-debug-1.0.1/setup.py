"""
Author: Nabil El Ouaamari (nabil.elouaamari.dev@gmail.com)
setup.py (c) 2023
Desc: A simple setup file for the colorful_debug module.
"""
from setuptools import setup

setup(
    name="colorful-debug",
    version="1.0.1",
    description="A colorful debug print module.",
    author="Nabil El Ouaamari",
    author_email="nabil.elouaamari.dev@gmail.com",
    packages=["colorful_debug"],
    install_requires=["termcolor"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
