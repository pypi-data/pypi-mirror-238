
import os
from setuptools import setup, find_packages

PACKAGE = "credential_sdk"
DESCRIPTION = "credential sdk"
AUTHOR = "kever"
VERSION = '0.0.3'
with open("README.md", "r") as fh:
    long_description = fh.read()

setup_args = {
    'version': VERSION,
    'description': DESCRIPTION,
    'author': AUTHOR,
    'license': "Apache License 2.0",
    'keywords': ["sdk", "tea"],
    'packages': find_packages(exclude=["tests*"]),
    'long_description': long_description,
    'long_description_content_type': "text/markdown",
    'platforms': 'any',
    'python_requires': '>=3.6',
    'classifiers': (
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development',
    )
}

setup(name='credential_sdk', **setup_args)
