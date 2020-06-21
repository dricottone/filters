#!/usr/bin/env python3

from setuptools import setup

long_description = None
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="filters",
    packages=["filter", "rng"],
    version="1.0.1",
    license="GPL",
    description="Data filters",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Dominic Ricottone",
    author_email="me@dominic-ricottone.com",
    url="git.dominic-ricottone.com/filters",
    entry_points={"console_scripts": ["filter = filter.__main__:main", "rng = rng.__main__:main"]},
    python_requires=">=3.6",
)

