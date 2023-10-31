#!/usr/bin/env python

from setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

name = "Markus Stahl"

version = os.environ.get('CI_COMMIT_TAG')

setup(
    name="robotframework-humanitec",
    version=version,
    description="Keywords for Humanitec REST api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=name,
    author_email="markus.i.sverige@googlemail.com",
    url="https://gitlab.com/noordsestern/robotframework-humanitec",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Framework :: Robot Framework :: Library",
        "Typing :: Typed"
    ],
    license="EUPL 1.2",
    install_requires=["robotframework", "requests", "unofficial-humanitec-client"],
    include_package_data=True,
)