#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    author="Alexander Lewzey",
    author_email='a.lewzey@hotmail.co.uk',
    python_requires='>=3.5',
    description="A collection of general purpose helper modules",
    entry_points={
        'console_scripts': [
            'audiotk=audiotk.cli:main',
        ],
    },
    install_requires=[
        'pydub',
        'fire',
    ],
    license="BSD license",
    keywords='audiotk',
    name='audiotk',
    packages=find_packages(include=['audiotk', 'audiotk.*']),
    test_suite='tests',
    url='https://github.com/alexlewzey/slibtk',
    version='0.1.0',
)
