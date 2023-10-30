#!/usr/bin/env python

import os
import setuptools

with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="sphinxcontrib-swaggerui",
    version="0.1.0",
    description="Provides the swaggerui directive for reST files to build an interactive HTML page with your OpenAPI specification document.",
    long_description=long_description,
    license='BSD',
    author="Albert Bagdasaryan",
    author_email="albert.bagd@gmail.com",
    packages=setuptools.find_packages(),
    include_package_data=True,
    url="https://bitbucket.org/albert_bagdasaryan/sphinxcontrib-swaggerui/",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: Sphinx :: Extension",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Documentation",
        "Topic :: Utilities"
    ],
    namespace_packages=['sphinxcontrib'],
)
