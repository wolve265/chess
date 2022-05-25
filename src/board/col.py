import pygame

from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface
from typing import *

from game import game
from settings import Settings


class Col(Group):
    """
    Class representing the board column
    """

    def __init__(self, col, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        self.col = col
        self.col_str = chr(self.col + ord('a'))
        self.full_rect_top = pygame.Rect((self.col*Settings.square_len + Settings.border_len, 0), (Settings.square_len, Settings.border_len))
        self.full_rect_bottom = pygame.Rect((self.col*Settings.square_len + Settings.border_len, Settings.board_len + Settings.border_len), (Settings.square_len, Settings.border_len))
        self.image = game.font.render(f"{self.col_str}", True, Settings.white_color)
        self.rect_top = self.image.get_rect(center=self.full_rect_top.center)
        self.rect_bottom = self.image.get_rect(center=self.full_rect_bottom.center)

    def __repr__(self) -> str:
        return f'{super().__repr__()} = {self.col}'

    def draw(self, surface: Surface) -> List[Rect]:
        surface.blit(self.image, self.rect_top)
        surface.blit(self.image, self.rect_bottom)
        return super().draw(surface)
