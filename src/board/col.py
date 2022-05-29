import pygame

from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface
from typing import *

import utils

from game import *
from settings import Settings


class Col(Group):
    """
    Class representing the board column
    """

    def __init__(self, col_i, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        self.col_i = col_i
        self.col_str = utils.col_int2str(self.col_i)
        self.full_rect_top = pygame.Rect((self.col_i*Settings.SQUARE_LEN + Settings.BORDER_LEN, 0), (Settings.SQUARE_LEN, Settings.BORDER_LEN))
        self.full_rect_bottom = pygame.Rect((self.col_i*Settings.SQUARE_LEN + Settings.BORDER_LEN, Settings.BOARD_LEN + Settings.BORDER_LEN), (Settings.SQUARE_LEN, Settings.BORDER_LEN))
        self.image = game.font.render(f"{self.col_str}", True, Settings.SQUARE_WHITE_COLOR)
        self.rect_top = self.image.get_rect(center=self.full_rect_top.center)
        self.rect_bottom = self.image.get_rect(center=self.full_rect_bottom.center)

    def __repr__(self) -> str:
        return f'{super().__repr__()} = {self.col_i}'

    def draw(self, surface: Surface) -> List[Rect]:
        surface.blit(self.image, self.rect_top)
        surface.blit(self.image, self.rect_bottom)
        return super().draw(surface)
