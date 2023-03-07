"""The setup script."""

import sys
from subprocess import check_call

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install

with open("README.md") as readme_file:
    readme = readme_file.read()


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        develop.run(self)
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        if sys.platform == "darwin":
            check_call("brew install ffmpeg".split())


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        if sys.platform == "darwin":
            check_call("brew install ffmpeg".split())


setup(
    author="Alexander Lewzey",
    author_email="a.lewzey@gmail.com",
    python_requires=">=3.5",
    description="A collection of general purpose helper modules",
    entry_points={
        "console_scripts": [
            "audiotk=audiotk.audiotk:main",
            "guitartk=audiotk.guitartk:main",
            "sample_organiser=audiotk.sample_organiser:main",
        ],
    },
    install_requires=[
        "pydub",
        "simpleaudio",
        "soundfile",
        "scipy",
        "matplotlib",
        "tqdm",
        "fire",
    ],
    license="BSD license",
    keywords="audiotk",
    name="audiotk",
    packages=find_packages(include=["audiotk", "audiotk.*"]),
    url="https://github.com/alexlewzey/audiotk",
    version="0.1.0",
    cmdclass={"develop": PostDevelopCommand, "install": PostInstallCommand,},
)
