from typing import Tuple


def rgb_to_int(rgb: Tuple[int, int, int]):
    return (rgb[0] << 16) | (rgb[1] << 8) | rgb[2]