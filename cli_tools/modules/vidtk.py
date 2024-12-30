from pathlib import Path

from moviepy.editor import VideoFileClip


def to_gif(path: str, width: int = 1000, fps: int = 10) -> None:
    path = Path(path)
    clip = VideoFileClip(path.as_posix()).resize(width=width)
    clip.write_gif(f"{path.stem}.gif", program="ffmpeg", fps=fps)
