#!/usr/bin/env python
from setuptools import setup

# See setup.cfg for configuration.
setup(
    package_data={
        'gpflib': ['gpflib.dll', 'libgpflib.so', 'config.txt', 'gpflib.py'],
    }
)

