#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#    my_project_template My Project Template.
#    Copyright (c) 2021 Be The Match operated by National Marrow Donor Program. All Rights Reserved.
#
#    This library is free software; you can redistribute it and/or modify it
#    under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation; either version 3 of the License, or (at
#    your option) any later version.
#
#    This library is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; with out even the implied warranty of MERCHANTABILITY or
#    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
#    License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this library;  if not, write to the Free Software Foundation,
#    Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA.
#
#    > http://www.fsf.org/licensing/licenses/lgpl.html
#    > http://www.opensource.org/licenses/lgpl-license.php
#


"""The setup script."""

from setuptools import setup, find_packages

setup(
    name="pyard",
    version="1.0.5",
    author="Pradeep Bashyal",
    author_email="pbashyal@nmdp.org",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="This is not the pyard you're looking for.",
    install_requires=None,
    license="LGPL 3.0",
    long_description="# Legacy pyard\n## This is not the `pyard` you're looking for.\nSee [py-ard](https://pypi.org/project/py-ard/) for the real deal.",
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=find_packages(include=["pyard"]),
    url="https://github.com/nmdp-bioinformatics/pyard-legacy",
    zip_safe=False
)
