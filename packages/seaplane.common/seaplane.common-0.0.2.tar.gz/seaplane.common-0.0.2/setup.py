# coding: utf-8

"""
    Seaplane Common

    Contact: support@seaplane.io
"""

from setuptools import setup, find_namespace_packages

NAME = "seaplane.common"
VERSION = "0.0.2"

REQUIRES = [
    "urllib3 >= 1.25.3",
]

setup(
    name=NAME,
    version=VERSION,
    author="Seaplane IO, Inc.",
    author_email="support@seaplane.io",
    url="",
    keywords=["Seaplane", "Common"],
    python_requires=">=3.8",
    install_requires=REQUIRES,
    packages=find_namespace_packages(include=["seaplane.*"]),
    include_package_data=True,
    license="Apache 2.0",
    description="",
    long_description="",
)
