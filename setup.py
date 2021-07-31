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
            'audiotk=audiotk.audiotk:main',
            'sample_organiser=audiotk.sample_organiser:main'
        ],
    },
    install_requires=[
        'pydub',
        'simpleaudio',
        'soundfile',
        'scipy',
        'matplotlib',
        'tqdm',
        'fire',
    ],
    license="BSD license",
    keywords='audiotk',
    name='audiotk',
    packages=find_packages(include=['audiotk', 'audiotk.*']),
    test_suite='tests',
    url='https://github.com/alexlewzey/audiotk',
    version='0.1.0',
)
