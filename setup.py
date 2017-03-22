# coding=utf-8
from __future__ import unicode_literals

from setuptools import setup, find_packages

setup(
    name="mit_moira",
    version="0.0.1",
    description="Library to access MIT's Moira service",
    long_description=open('README.rst').read(),
    author="David Baumgold",
    author_email="david@davidbaumgold.com",
    packages=find_packages(),
    install_requires=[
        "zeep"
    ],
    license='MIT',
)
