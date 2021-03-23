#! /usr/bin/env python

import os
from setuptools import setup
import sys

# Additional keyword arguments for setup().
extra = {}

# Ordinary dependencies
DEPENDENCIES = []
with open("requirements/requirements-all.txt", "r") as reqs_file:
    for line in reqs_file:
        if not line.strip():
            continue
        DEPENDENCIES.append(line)

with open("pepconvert/_version.py", 'r') as versionfile:
    version = versionfile.readline().split()[-1].strip("\"'\n")

# Handle the pypi README formatting.
with open('README.md') as f:
    long_description = f.read()

setup(
    name="pepconvert",
    packages=["pepconvert"],
    version=version,
    description="Converts PEP sample metadata into different formats.",
    long_description=long_description,
    long_description_content_type='text/markdown', 
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
    keywords="bioinformatics, sequencing, ngs",
    url="https://github.com/pepkit/pepconvert",
    author=u"Nathan Sheffield",
    license="BSD2",
    entry_points={
        "console_scripts": [
            'pepconvert = pepconvert.__main__:main'
        ],
        'pep.filters': 'basic=pepconvert:my_basic_plugin',
    },
    include_package_data=True,
    test_suite="tests",
    tests_require=(["mock", "pytest"]),
    setup_requires=(["pytest-runner"] if {"test", "pytest", "ptr"} & set(sys.argv) else []),
    **extra
)
