"""Conda install -c conda-forge ffmpeg."""

from pathlib import Path

import fire
import matplotlib.pyplot as plt
import pydub
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play
from pydub.utils import make_chunks
from scipy.io.wavfile import read
from tqdm import tqdm

# pydub.AudioSegment.converter = r"C:\Users\alewz\miniconda3\Library\bin\ffmpeg.exe"
# pydub.AudioSegment.ffmpeg = r"C:\Users\alewz\miniconda3\Library\bin\ffmpeg.exe"


def tag_sample(sample: Path) -> str:
    """Assign a sample file to a folder eg (kick, snare etc) returning folder
    as a string."""
    for hat_type in ["open", "closed"]:
        if all([item in sample.name for item in (hat_type, "hat")]):
            return f"hat_{hat_type}"

    find = {
        "clap": ["clap", "clp"],
        "ride": ["ride"],
        "snare": ["snare", "snr"],
        "tom": ["tom"],
        "bongo": ["bongo"],
        "shaker": ["shaker"],
        "rim": ["rim"],
        "kick": ["kick", "bd", "bassdrum"],
        "hat_closed": ["hhc", "closed"],
        "hat_open": ["open", "hho"],
        "hat": ["hat", "hh"],
        "cymbal": ["cymbal"],
        "perc_misc": ["perc"],
    }
    for kit, substrings in find.items():
        if any([s in sample.name.lower() for s in substrings]):
            return kit
    return "none"


def plot_wave(path: Path, title: str | None = None) -> tuple:
    """Plot a waveform with plotly."""
    input_data = read(path.as_posix())
    audio = input_data[1]
    fig, ax = plt.subplots()
    ax.plot(audio)
    plt.title(title if title else path.name)
    plt.ion()
    plt.show()
    return fig, ax


def user_tag_check(cwd: Path, sample: Path) -> str | None:
    """Allows the user to visually and audibly check the destination dir
    assigned to the sample and override it if required."""
    dirs = [
        path
        for path in cwd.iterdir()
        if path.is_dir() and not path.name.startswith((".", "__"))
    ]
    index = dict(enumerate(dirs))
    dirs = "\n".join([f"{n}: {dname}" for n, dname in index.items()])

    demo_sample, temp = sample, cwd / "temp.wav"

    # if sample is mp3 format
    if sample.suffix == ".mp3":
        clip = AudioSegment.from_mp3(sample.as_posix()).export(temp, format="wav")
        clip.close()
        demo_sample = temp

    # if sample has bit depth of 24 save as 16 before playing / plotting, pydub & scipy do not support 24 bit
    sound_file = sf.SoundFile(demo_sample.as_posix())
    if sound_file.subtype in ("PCM_24", "FLOAT"):
        data, sample_rate = sf.read(demo_sample.as_posix())
        sf.write(temp.as_posix(), data, sample_rate, subtype="PCM_16")
        demo_sample = temp
    sound_file.close()

    clip = AudioSegment.from_wav(demo_sample.as_posix())
    chunk_length_ms = 5000  # 5 seconds
    clip = make_chunks(clip, chunk_length_ms)[0]  # Make chunks of one sec

    pydub.playback._play_with_simpleaudio(clip)
    fig, _ = plot_wave(demo_sample, title=sample.name)

    file_tag = tag_sample(sample)
    hat_index = dict(enumerate(["hat_closed", "hat_open", "hat_misc"]))
    hat_menu = "\n".join([f"{i}: {nm}" for i, nm in hat_index.items()])

    while True:
        dest = (
            input(f"Destinations:\n{dirs}\n\n{sample.name} to [{file_tag}]: ")
            or file_tag
        )
        if dest == "r":
            play(clip)
            continue
        if dest == "s":
            dest = "skipped"
        try:
            if int(dest) in index.keys():
                dest = index[int(dest)]
        except ValueError:
            pass
        if dest == "hat":
            idx = int(input(f"Hat types:\n{hat_menu}\n\nWhich hat type: "))
            dest = hat_index[idx]
        break
    plt.close(fig)
    if temp.exists():
        temp.unlink()
    return dest


def move_sample(cwd: Path, sample: Path, dest_dir: str) -> None:
    """Move sample file to allocated destination dir."""
    dest_path = cwd / dest_dir / sample.name
    try:
        sample.rename(Path(dest_path.as_posix()))
    except FileExistsError:
        path_duplicate: Path = dest_path.parent / (
            dest_path.stem + "_dub" + dest_path.suffix
        )
        print(f"renaming as duplicate: {path_duplicate.as_posix()}")
        sample.rename(path_duplicate)
    print("file moved: " + sample.name + " > " + dest_path.as_posix())


def is_sample_file(sample: Path | None) -> bool | None:
    if sample:
        return (
            sample.is_file()
            and not sample.name.endswith((".asd", ".py"))
            and not sample.name.startswith(".")
        )


def allocate_sample(cwd: Path | str, sample: Path) -> None:
    """Assigen sample to folder > get user to check destination with option to
    override.

    > move .asd file if one exists
    """
    dest = user_tag_check(cwd=cwd, sample=sample)
    if dest:
        move_sample(cwd=cwd, sample=sample, dest_dir=dest)
        sample_asd = Path(sample.as_posix() + ".asd")
        if sample_asd.exists():
            move_sample(sample=sample_asd, dest_dir=dest, cwd=cwd)


def organiser(cwd: Path | str) -> None:
    """"""
    cwd = Path(cwd)
    samples = [path for path in cwd.iterdir() if is_sample_file(path)]
    for sample in tqdm(samples):
        allocate_sample(cwd, sample)


def main():
    fire.Fire(organiser)
