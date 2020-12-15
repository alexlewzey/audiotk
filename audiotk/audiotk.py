"""command line tool for interacting with audio files"""
from pathlib import Path
from typing import *

import fire
from pydub import AudioSegment
import re


def audio2fmt(path: Union[str, Path], fmt: str) -> None:
    """
    save every file in a directory to an arg format
    Args:
        path: directory containing audio files
        fmt: output file extension eg wav

    """
    path = Path(path)
    for f in path.iterdir():
        if f.is_file():
            suffix = f.suffix.strip('.')
            if suffix not in [fmt, 'py', 'mid', 'asd', '']:
                clip = AudioSegment.from_file(f.as_posix(), format=suffix)
                out_path = (f.parent / f'{f.stem}.{fmt}').as_posix()
                clip.export(out_path, format=fmt)


def audio2wav(path: Union[str, Path]) -> None:
    audio2fmt(path, 'wav')


def prune(path: Union[str, Path], safe: bool = True) -> None:
    """remove every file in the path that does is not a wav, py or asd file type"""
    path = Path(path)
    for f in path.iterdir():
        if f.suffix not in ['.wav', '.py', '.asd', '.mid']:
            if safe:
                input(f'delete: {f.name}')
            print(f'removing file: {f.name}')
            f.unlink()


def ls(path: Union[str, Path]):
    """list of the unique file stems in the directory"""
    path = Path(path)
    fnames = [re.search('(.+?)\..+', p.name).groups()[0] for p in path.iterdir()]
    for fn in set(fnames):
        print(fn)


if __name__ == '__main__':
    fire.Fire({
        'audio2fmt': audio2fmt,
        'audio2wav': audio2wav,
        'prune': prune,
        'ls': ls,
    })
