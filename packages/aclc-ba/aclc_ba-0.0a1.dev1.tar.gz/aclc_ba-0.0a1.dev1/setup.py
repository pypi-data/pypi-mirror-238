# -*- coding: utf-8 -*-
# Copyright (C) 2023 Bibliotheca Alexandrina <www.bibalex.org>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import find_packages, setup


def readme():
    with open("README.rst") as f:
        return f.read()

with open(os.path.join(os.path.dirname(__file__), 'aclc_ba','VERSION')) as version_file:
    VERSION = version_file.read().strip()

setup(
    name="aclc_ba",
    url="https://github.com/ba-aclc",
    description="Arabic Processing tool",
    long_description_content_type="text/x-rst",
    long_description=readme(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: Arabic",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Linguistic",
    ],
    author="Arabic Computational Linguistics Centre at BA",
    license="GNU",
    dependency_links=["http://github.com/user/repo/tarball/master#egg=package-1.0"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    extras_require = {
        "dev":["pytest>=7.0", "twine>=4.0.2"],
        },
    package_data={},
    entry_points={
        "console_scripts": [],
    },
    python_requires=">= 3.7",
    version=VERSION,
)


