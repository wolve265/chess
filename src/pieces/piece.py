from pygame.sprite import AbstractGroup
from typing import *

from board.square import Square
from game import game
from settings import Settings


class Piece(Square):
    """
    Abstract class for every piece
    """

    def __init__(self, row: int, col: int, is_white: bool, *groups: AbstractGroup) -> None:
        super().__init__(row, col, *groups)
        self.is_white = is_white
        self.color = Settings.white_piece_color if is_white else Settings.black_piece_color
        self.background_color = Settings.black_piece_color if is_white else Settings.white_piece_color
        self.value = ''
        self.image = game.font.render(f"", True, self.color)
        self.rect = self.image.get_rect(center=self.full_rect.center)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.image = game.font.render(f"{self.value}", True, self.color, self.background_color)
        self.rect = self.image.get_rect(center=self.full_rect.center)
        return super().update(*args, **kwargs)
