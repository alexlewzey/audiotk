"""command line tool for interacting with audio files"""

import re

import fire
from pydub import AudioSegment, effects

from audiotk.core import *


def normalise(*paths: PathOrStr) -> None:
    """normalise an arbitrary number of audio file"""
    for path in paths:
        path = Path(path)
        suffix = path.suffix.strip('.')
        clip = effects.normalize(AudioSegment.from_file(path.as_posix(), suffix))
        clip.export(path.as_posix(), format=suffix)
        print(f'normalised: {path.as_posix()}')


def normaliser(path: PathOrStr, fmt: str) -> None:
    """normalise every file in a directory of a particular audio format"""
    for p in Path(path).iterdir():
        if p.is_file() and p.suffix.strip('.') == fmt:
            clip = effects.normalize(AudioSegment.from_file(path.as_posix(), fmt))
            clip.export(path.as_posix(), format=fmt)
            print(f'normalised: {p.as_posix()}')


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
        'normalise': normalise,
        'normaliser': normaliser,
        'fmt2fmt': fmt2fmt,
        'm4a2wav': m4a2wav,
        'mp32wav': mp32wav,
        'prune': prune,
        'ls': ls,
    })
