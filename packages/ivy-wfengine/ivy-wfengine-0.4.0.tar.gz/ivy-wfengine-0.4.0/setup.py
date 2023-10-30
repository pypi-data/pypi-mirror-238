#!/usr/bin/env python

import os

from setuptools import find_packages, setup


requirements = []


with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read().replace(".. :changelog", "")


doclink = """
Documentation
-------------

The full documentation can be generated with Sphinx"""


PACKAGE_PATH = os.path.abspath(os.path.join(__file__, os.pardir))

setup(
    name="ivy-wfengine",
    version="0.4.0",
    description="Simple and flexible workflow engine",
    long_description=readme + "\n\n" + doclink + "\n\n" + history,
    long_description_content_type="text/x-rst",
    author="Joel Akeret",
    author_email="jakeret@phys.ethz.ch",
    url="https://cosmo-gitlab.phys.ethz.ch/cosmo/ivy",
    package_dir={"ivy": "ivy"},
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="Proprietary",
    zip_safe=False,
    keywords="ivy",
    entry_points={
        "console_scripts": [
            "ivy = ivy.cli.main:run",
        ]
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
    ],
)
