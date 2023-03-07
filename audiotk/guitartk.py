"""What note corresponds to the nth fret of the nth string?"""
import random
import time

import fire

fifths = ["C", "G", "D", "A", "E", "B", "Gb", "Db", "Ab", "Eb", "Bb", "F", "C"]
fourths = reversed(fifths)
print(" ".join(fourths))
chromatic = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
notes = ["C", "D", "E", "F", "G", "A", "B"]
sharps = ["C#", "D#", "F#", "G#", "B#"]
flats = ["Db", "Eb", "Gb", "Ab", "Bb"]
scales = ["Major", "Minor"]
directions = ["up", "down", "left", "right"]
modes = ["ionian", "dorian", "phrygian", "lydian", "mixolydian", "aeolian", "locrian"]


def rand_fretboard_position(start=1, end=6):
    """Return random fretboard position e.g. string: 5, fret 12."""
    while True:
        print(
            f"string: {random.randint(start, end):02} fret:{random.randint(0, 12):02}",
            end="\r",
        )
        time.sleep(4)


def rand_loop(notes, rest: float | None = None) -> None:
    while True:
        print(random.choice(notes))
        time.sleep(rest) if rest else input("")


def rand_note(rest: float = 5.0):
    """Return a random note e.g. A."""
    rand_loop(chromatic, rest)


def rand_fifth(rest: float = 0.9):
    rand_loop(fifths, rest)


def rand_note_and_scale() -> None:
    while True:
        print(f"{random.choice(chromatic)} {random.choice(scales)}")
        input("")


def rand_note_and_direction() -> None:
    while True:
        print(f"{random.choice(chromatic)} {random.choice(directions)}")
        input("")


def main():
    fire.Fire(
        {"fb_pos": rand_fretboard_position, "rand_note": rand_note,}
    )
