from pygame.sprite import AbstractGroup
from pygame.surface import Surface
from typing import *

from game import game
from settings import Settings
from square import Square


class Piece(Square):
    def __init__(self, row: int, col: int, is_white: bool, *groups: AbstractGroup) -> None:
        super().__init__(row, col, *groups)
        self.is_white = is_white
        self.color = Settings.white_piece_color if is_white else Settings.black_piece_color
        self.image = game.font.render(f"{self.value}", True, self.color)
        self.rect = self.image.get_rect(center=self.full_rect.center)

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)
