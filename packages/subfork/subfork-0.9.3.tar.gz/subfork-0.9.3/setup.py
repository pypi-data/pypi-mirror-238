#!/usr/bin/env python
#
# Copyright (c) 2022-2023 Subfork. All rights reserved.
#

import os
import sys
import codecs
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), "r").read()


exec(read("lib", "subfork", "version.py"))


def get_scripts():
    if sys.platform == "win32":
        return ["bin/subfork", "bin/subfork.bat"]
    return ["bin/subfork", "bin/worker"]


setup(
    name="subfork",
    description="Subfork Python API",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Subfork",
    author_email="help@subfork.com",
    version=__version__,
    license="BSD 3-Clause License",
    package_dir={"": "lib"},
    packages=find_packages("lib"),
    scripts=get_scripts(),
    install_requires=[
        "jsmin==3.0.1",
        "psutil==5.9.3",
        "PyYAML==5.3.1",
        "requests==2.25.1",
        "urllib3==1.26.3",
    ],
    data_files=[
        (
            "/subfork/data",
            [
                "example_subfork.yaml",
                "services/worker.service",
            ],
        ),
    ],
    zip_safe=False,
)
