#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="django-datatables",
    version="0.1.0",
    description="",
    author="Sam Jennings",
    author_email="samuel.scott.jennings@gmail.com",
    url="https://github.com/SSJenny90/django-datatables",
    packages=[
        "datatables",
    ],
    include_package_data=True,
    install_requires=[],
    license="MIT",
    zip_safe=False,
    keywords="django,datatables,geoluminate,scientific",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django :: 3.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
