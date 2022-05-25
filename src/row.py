import pygame

from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface
from typing import *

from game import game
from settings import Settings


class Row(Group):
    def __init__(self, row, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        self.row = row
        self.row_str = chr(self.row + ord('1'))
        self.full_rect_left = pygame.Rect((0, (Settings.rows-self.row-1)*Settings.square_len + Settings.border_len), (Settings.border_len, Settings.square_len))
        self.full_rect_right = pygame.Rect((Settings.board_len + Settings.border_len, (Settings.rows-self.row-1)*Settings.square_len + Settings.border_len), (Settings.border_len, Settings.square_len))
        self.image = game.font.render(f"{self.row_str}", True, Settings.white_color)
        self.rect_left = self.image.get_rect(center=self.full_rect_left.center)
        self.rect_right = self.image.get_rect(center=self.full_rect_right.center)

    def __repr__(self) -> str:
        return f'{super().__repr__()} = {self.row}'

    def draw(self, surface: Surface) -> List[Rect]:
        surface.blit(self.image, self.rect_left)
        surface.blit(self.image, self.rect_right)
        return super().draw(surface)
