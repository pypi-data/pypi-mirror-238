# -*- coding: utf-8 -*-

from os import path
import re
from setuptools import setup

package_name = "dfcon"

root_dir = path.abspath(path.dirname(__file__))


def _requirements():
    return [
        name.rstrip()
        for name in open(
            path.join(root_dir, "requirements.txt"), encoding="utf-8"
        ).readlines()
    ]


def _test_requirements():
    return [
        name.rstrip()
        for name in open(
            path.join(root_dir, "test-requirements.txt"), encoding="utf-8"
        ).readlines()
    ]


with open(path.join(root_dir, package_name, "__init__.py"), encoding="utf-8") as f:
    init_text = f.read()
    version = re.search(r"__version__\s*=\s*[\'\"](.+?)[\'\"]", init_text).group(1)
    license_ = re.search(r"__license__\s*=\s*[\'\"](.+?)[\'\"]", init_text).group(1)
    author = re.search(r"__author__\s*=\s*[\'\"](.+?)[\'\"]", init_text).group(1)
    author_email = re.search(
        r"__author_email__\s*=\s*[\'\"](.+?)[\'\"]", init_text
    ).group(1)
    url = re.search(r"__url__\s*=\s*[\'\"](.+?)[\'\"]", init_text).group(1)

assert version
assert license_
assert author
assert author_email
assert url

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name=package_name,
    packages=["dfcon"],
    version=version,
    license=license_,
    install_requires=_requirements(),
    tests_require=_test_requirements(),
    author=author,
    author_email=author_email,
    url=url,
    description="To make access to the database easier.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="DataSet, File-Search, File-Controle",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
