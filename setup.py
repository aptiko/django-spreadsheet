#!/usr/bin/env python
import os
import re

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = [
    "django>=2.2,<4",
    "openpyxl>=3,<4",
]

test_requirements = []


def get_version():
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    init_py_path = os.path.join(scriptdir, "django_spreadsheet", "__init__.py")
    with open(init_py_path) as f:
        return re.search(r'^__version__ = "(.*?)"$', f.read(), re.MULTILINE).group(1)


setup(
    author="Antonis Christofides",
    author_email="antonis@antonischristofides.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="Create a spreadsheet from the database with minimal code",
    install_requires=requirements,
    license="BSD license",
    long_description=readme,
    include_package_data=True,
    keywords="django-spreadsheet",
    name="django-spreadsheet",
    packages=find_packages(include=["django_spreadsheet", "django_spreadsheet.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/aptiko/django-spreadsheet",
    version=get_version(),
    zip_safe=False,
)
