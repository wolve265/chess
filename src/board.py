from itertools import product
from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface
from typing import *

from game import game
from square import Square
from settings import Settings


class Board(Group):
    def __init__(self, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        self.squares = self.gen_squares()
        super().__init__(self.squares, *sprites)

    def draw(self, surface: Surface) -> List[Rect]:
        game.screen.fill('White')
        for square in self.squares:
            square.draw(surface)
        return super().draw(surface)

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)

    def gen_squares(self) -> List[Square]:
        squares: List[Square] = []
        for row, col in product(range(Settings.rows), range(Settings.cols)):
            squares.append(Square(row, col))
        return squares
