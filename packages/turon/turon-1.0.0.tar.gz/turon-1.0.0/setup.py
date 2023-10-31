#!/usr/bin/env python
import os
import re

from distutils.core import setup
from setuptools import find_packages


INSTALL_REQUIREMENTS = [
    'pandas>2,<3',
    'requests>2,<3',
]


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


setup(
    name='turon',
    version=get_version('turon'),
    description='Python adapter for turon.io',
    author='Scott Cruwys',
    author_email='scott@turon.io',
    url='https://ww.github.com/tryturon/turon-py',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=INSTALL_REQUIREMENTS,
    python_requires='==3.8.*',
)
