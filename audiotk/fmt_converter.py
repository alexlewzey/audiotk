"""command line tool for interacting with audio files"""
from pathlib import Path
from typing import *

import fire
from pydub import AudioSegment
import re


def fmt2fmt(path: Union[str, Path], in_fmt: str, out_fmt: str) -> None:
    """
    covert every file in a directory of a particular format to another format and remove the original
    Args:
        path: directory containing audio files
        in_fmt: input file extension eg m4a
        out_fmt: output file extension eg wav

    """
    for in_path in Path(path).iterdir():
        if in_path.is_file() and in_path.suffix.strip('.') == in_fmt:
            clip = AudioSegment.from_file(in_path.as_posix(), format=in_fmt)
            out_path = in_path.parent / f'{in_path.stem}.{out_fmt}'
            clip.export(out_path.as_posix(), format=out_fmt)
            print(f'coverted: {in_path.name} > {out_path.as_posix()}')
            in_path.unlink()


def m4a2wav(path: Union[str, Path]) -> None:
    fmt2fmt(path, in_fmt='m4a', out_fmt='wav')


def mp32wav(path: Union[str, Path]) -> None:
    fmt2fmt(path, in_fmt='mp3', out_fmt='wav')


def prune(path: Union[str, Path], fmt: str) -> None:
    """remove every file in the path that does is not a wav, py or asd file type"""
    for f in Path(path).iterdir():
        if f.suffix.strip('.') == fmt:
            print(f'removing file: {f.name}')
            f.unlink()


def ls(path: Union[str, Path]):
    """list of the unique file stems in the directory"""
    path = Path(path)
    fnames = [re.search('(.+?)\..+', p.name).groups()[0] for p in path.iterdir()]
    for fn in set(fnames):
        print(fn)


def main():
    fire.Fire({
        'fmt2fmt': fmt2fmt,
        'm4a2wav': m4a2wav,
        'mp32wav': mp32wav,
        'prune': prune,
        'ls': ls,
    })
