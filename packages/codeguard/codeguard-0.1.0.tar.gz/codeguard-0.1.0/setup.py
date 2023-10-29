# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 11:44:12 2023

@author: DeepakKumar
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codeguard",
    version="0.1.0",
    author="Deepak Kumar",
    description="Destroys the code in which this library is being called. The purpose of this code is to allow your main code to run for a specified time, after which it prevents further use of your main code beyond the agreed time.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Deep776/codeguard",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)