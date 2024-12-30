"""Command line tool for interacting with audio files.

instructions
------------

1. install package with pip: pip install -e .
2. setup.py includes and entry point so scripts can be run from the command line
3. convert files in current directory: fmt_converter m4a2wav .
"""

import subprocess
import sys

import fire

from .modules import audiotk, imgtk, vidtk

if sys.platform == "darwin":
    try:
        commands = ["ffmpeg", "-version"]
        subprocess.run(commands, check=True, stdout=subprocess.PIPE)  # noqa: S603
    except subprocess.CalledProcessError:
        print(
            "ffmpeg is required to run this app on mac. Please install ffmpeg: brew "
            "install ffmpeg"
        )
        sys.exit(1)


def main():
    fire.Fire(
        {
            "normalise": audiotk.normalise,
            "normaliser": audiotk.normaliser,
            "fmt2fmt": audiotk.fmt2fmt,
            "m4a2wav": audiotk.m4a2wav,
            "mp32wav": audiotk.mp32wav,
            "prune": audiotk.prune,
            "speech2text": audiotk.speech2text,
            "to_gif": vidtk.to_gif,
            "recolor": imgtk.recolor,
        }
    )
