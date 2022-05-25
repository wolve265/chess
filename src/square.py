import pygame

from pygame.sprite import AbstractGroup, Sprite
from pygame.surface import Surface
from typing import *

from game import game
from settings import Settings


class Square(Sprite):

    def __init__(self, row: int, col: int, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.row = row
        self.col = col
        self.row_str = chr(self.row + ord('1'))
        self.col_str = chr(self.col + ord('a'))
        self.full_rect = pygame.Rect((self.col*Settings.square_len + Settings.border_len, (Settings.rows-self.row-1)*Settings.square_len + Settings.border_len), Settings.square_size)
        self.image = game.font.render(f"", True, 'Red')
        self.rect = self.image.get_rect(center=self.full_rect.center)

    def __repr__(self) -> str:
        return f'\n{super().__repr__()} | pos = ({self.col_str},{self.row_str})'

    def draw(self, surface: Surface) -> None:
        fill_color = Settings.white_color if (self.row + self.col) % 2 else Settings.black_color
        pygame.draw.rect(surface, fill_color, self.full_rect)

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)
