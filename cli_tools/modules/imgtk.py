from PIL import Image
from pydantic import BaseModel, Field


class RGB(BaseModel):
    r: int = Field(ge=0, le=255)
    g: int = Field(ge=0, le=255)
    b: int = Field(ge=0, le=255)

    def to_tuple(self) -> tuple[int, int, int]:
        return (self.r, self.g, self.b)


def recolor(input_path: str, output_path: str, rgb: tuple[int, int, int]) -> None:
    RGB(r=rgb[0], g=rgb[1], b=rgb[2])
    img = Image.open(input_path)
    img = img.convert("RGBA")
    pixels = img.getdata()
    new_pixels = []
    for item in pixels:
        if item[3] > 0:  # (R,G,B,A) if non-transparant pixel
            new_pixels.append((*rgb, item[3]))
        else:
            new_pixels.append(item)
    img.putdata(new_pixels)
    img.save(output_path)
