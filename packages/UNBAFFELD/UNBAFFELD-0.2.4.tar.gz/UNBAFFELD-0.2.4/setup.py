#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = [
    "inference-tools>=0.12.0",
    "numpy>=1.8",
    "scipy>=1.6.3",
    "h5py",
    "matplotlib>=3.4.2"
]

test_requirements = [
    "inference-tools>=0.12.0"
    # TODO: put package test requirements here
]

setup(
    name="unbaffeld",
    version="v0.2.4",
    description="UNified Bayesian Analysis Framework for Fusion ExperimentaL Data",
    long_description=readme + "\n\n",
    author="EFIT-AI Team",
    author_email="scott.e.kruger@gmail.com",
    url="https://gitlab.com/efit-ai/unbaffeld",
    packages=[
        "unbaffeld",
    ],
    package_dir={"unbaffeld": "unbaffeld"},
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords="unbaffeld",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Users",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    test_suite="tests",
    tests_require=test_requirements,
)
