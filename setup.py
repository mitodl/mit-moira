# coding=utf-8
from __future__ import unicode_literals

from setuptools import setup, find_packages

setup(
    name="mit-moira",
    version="0.0.1",
    description="Library to access MIT's Moira service",
    long_description=open('README.rst').read(),
    url="https://github.com/mitodl/mit-moira",
    author="MIT Office of Digital Learning",
    author_email="odl@mit.edu",
    packages=find_packages(),
    py_modules=['mit_moira'],
    install_requires=[
        "zeep"
    ],
    license='BSD',
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Topic :: Internet",
    ]
)
