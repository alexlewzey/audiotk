"""Command line tool for interacting with audio files.

instructions
------------

1. install package with pip: pip install -e .
2. setup.py includes and entry point so scripts can be run from the command line
3. convert files in current directory: fmt_converter m4a2wav .
"""

import re
from pathlib import Path

import fire
from pydub import AudioSegment, effects


def normalise(*paths: Path | str) -> None:
    """Normalise an arbitrary number of audio file."""
    for path in paths:
        path = Path(path)
        suffix = path.suffix.strip(".")
        clip = effects.normalize(AudioSegment.from_file(path.as_posix(), suffix))
        clip.export(path.as_posix(), format=suffix)
        print(f"normalised: {path.as_posix()}")


def normaliser(path: Path | str, fmt: str) -> None:
    """Normalise every file in a directory of a particular audio format."""
    for p in Path(path).iterdir():
        if p.is_file() and p.suffix.strip(".") == fmt:
            clip = effects.normalize(AudioSegment.from_file(p.as_posix(), fmt))
            clip.export(p.as_posix(), format=fmt)
            print(f"normalised: {p.as_posix()}")


def fmt2fmt(path: str | Path, in_fmt: str, out_fmt: str, norm: bool = True) -> None:
    """
    covert every file in a directory of a particular format to another format and remove the original
    Args:
        path: directory containing audio files
        in_fmt: input file extension eg m4a
        out_fmt: output file extension eg wav
        norm: bool if True normalise the audio once converted to new format

    """
    for in_path in Path(path).iterdir():
        if in_path.is_file() and in_path.suffix.strip(".") == in_fmt:
            clip = AudioSegment.from_file(in_path.as_posix(), format=in_fmt)
            out_path = in_path.parent / f"{in_path.stem}.{out_fmt}"
            clip.export(out_path.as_posix(), format=out_fmt)
            print(f"coverted: {in_path.name} > {out_path.as_posix()}")
            in_path.unlink()
            if norm:
                normalise(out_path)


def m4a2wav(path: str | Path, **kwargs) -> None:
    fmt2fmt(path, in_fmt="m4a", out_fmt="wav", **kwargs)


def mp32wav(path: str | Path) -> None:
    fmt2fmt(path, in_fmt="mp3", out_fmt="wav")


def prune(path: str | Path, fmt: str) -> None:
    """Remove every file in the path that does is not a wav, py or asd file
    type."""
    for f in Path(path).iterdir():
        if f.suffix.strip(".") == fmt:
            print(f"removing file: {f.name}")
            f.unlink()


def ls(path: str | Path):
    """List of the unique file stems in the directory."""
    path = Path(path)
    fnames = [re.search(r"(.+?)\..+", p.name).groups()[0] for p in path.iterdir()]
    for fn in set(fnames):
        print(fn)


def main():
    fire.Fire(
        {
            "normalise": normalise,
            "normaliser": normaliser,
            "fmt2fmt": fmt2fmt,
            "m4a2wav": m4a2wav,
            "mp32wav": mp32wav,
            "prune": prune,
            "ls": ls,
        }
    )
