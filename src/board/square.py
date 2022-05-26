import pygame

from pygame import Rect
from pygame.color import Color
from pygame.sprite import AbstractGroup, Sprite
from pygame.surface import Surface
from typing import *

import utils

from game import *
from settings import Settings


class Square(Sprite):
    """
    Class representing the single square of the chessboard
    """

    def __init__(self, row_i: int, col_i: int, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.row_i = row_i
        self.col_i = col_i
        self.color = self.get_color()
        self.full_rect = self.get_full_rect()
        self.image = game.font.render(f"", True, 'Red')
        self.rect = self.image.get_rect(center=self.full_rect.center)

    def __repr__(self) -> str:
        row_str = utils.row_int2str(self.row_i)
        col_str = utils.col_int2str(self.col_i)
        return f'\n{super().__repr__()} | pos = ({col_str},{row_str})'

    def draw(self, surface: Surface) -> None:
        pygame.draw.rect(surface, self.color, self.full_rect)

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)

    def get_color(self) -> Color:
        return Settings.white_color if (self.row_i + self.col_i) % 2 else Settings.black_color

    def get_full_rect(self) -> Rect:
        return pygame.Rect((self.col_i*Settings.square_len + Settings.border_len, (Settings.rows-self.row_i-1)*Settings.square_len + Settings.border_len), Settings.square_size)

    def select(self) -> None:
        self.color = utils.highlight_color(self.color)

    def deselect(self) -> None:
        self.color = self.get_color()
