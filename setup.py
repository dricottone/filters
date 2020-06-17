#!/usr/bin/env python3

from setuptools import setup

long_description = None
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="filter",
    packages=["filter"],
    version="1.0.0",
    license="GPL",
    description="Data filters",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Dominic Ricottone",
    author_email="me@dominic-ricottone.com",
    url="git.dominic-ricottone.com/gap",
    entry_points={"console_scripts": ["filter = filter.__main__:main"]},
    python_requires=">=3.6",
)

