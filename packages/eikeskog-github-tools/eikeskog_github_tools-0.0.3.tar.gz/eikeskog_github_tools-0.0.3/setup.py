#!/usr/bin/env python3

__author__ = "Svein Tore Eikeskog"
__email__ = "st@eikeskog.com"

import setuptools

setuptools.setup(
    name="eikeskog_github_tools",
    version="0.0.3",
    author=__author__,
    author_email=__email__,
    description="Use github api to perform tasks, e.g. check pr status, create milestone..",
    packages=["eikeskog_github_tools"],
    install_requires=["requests"]
)
