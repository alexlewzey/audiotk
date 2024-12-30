import shutil
from pathlib import Path

import pandas as pd
import pytest
from PIL import Image
from pydantic import ValidationError

from cli_tools.modules.imgtk import RGB, recolor


@pytest.fixture
def tmp_dir():
    tmp_dir = Path("tmp")
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(exist_ok=True)
    yield tmp_dir
    shutil.rmtree(tmp_dir)


def test_recolor(tmp_dir):
    input_path = Path("images") / "dog_logo.png"
    assert input_path.exists(), "Input test image not found"
    output_path = tmp_dir / "dog_logo_recolored.png"

    new_rgbs: list[tuple[int, int, int]] = [
        (255, 255, 255),
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (0, 0, 0),
    ]
    for new_rgb in new_rgbs:
        recolor(input_path=input_path, output_path=output_path, rgb=new_rgb)

        result_img = Image.open(output_path)
        result_pixels = result_img.convert("RGBA").getdata()
        result_color_dist = (
            pd.Series(list(result_pixels))
            .value_counts(dropna=False, normalize=True)
            .to_dict()
        )
        pct_transparent = result_color_dist[(0, 0, 0, 0)]
        new_rgba = new_rgb + (255,)
        pct_white = result_color_dist[new_rgba]
        assert 0.9 < pct_transparent < 0.91
        assert 0.07 < pct_white < 0.08


class TestRGB:
    def test_valid_rgb(self):
        input_ = (255, 255, 255)
        result = RGB(r=input_[0], g=input_[1], b=input_[2])
        assert result.to_tuple() == input_

    def test_invalid_rgb_bounds(self):
        with pytest.raises(ValidationError):
            input_ = (255, 255, 300)
            RGB(r=input_[0], g=input_[1], b=input_[2])

        with pytest.raises(ValidationError):
            input_ = (-1, 255, 255)
            RGB(r=input_[0], g=input_[1], b=input_[2])

    def test_missing_arg(self):
        with pytest.raises(ValidationError):
            input_ = (255, 255)
            RGB(r=input_[0], g=input_[1])
