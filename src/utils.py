import os
import pygame

from pygame.color import Color
from pygame.surface import Surface

dirname = os.path.dirname
join = os.path.join


def load_image(path: str) -> Surface:
    return pygame.image.load(path).convert_alpha()


def row_int2str(row_i: int) -> str:
    """
    Converts row index to string\n
    e.g 0 -> '1'
    """
    return chr(row_i + ord("1"))


def row_str2int(row_str: str) -> int:
    """
    Converts row string to index\n
    e.g '1' -> 0
    """
    return ord(row_str) - ord("1")


def col_int2str(col_i: int) -> str:
    """
    Converts column index to string\n
    e.g 0 -> 'a'
    """
    return chr(col_i + ord("a"))


def col_str2int(col_str: str) -> int:
    """
    Converts column string to index\n
    e.g 'a' -> 0
    """
    return ord(col_str) - ord("a")


def highlight_color(color: Color) -> Color:
    """
    Returns highlighted color
    """
    more_gamma = any([val > 0.8 for val in color.normalize()][:3])
    gamma = 5 if more_gamma else 2
    return color.correct_gamma(gamma)
