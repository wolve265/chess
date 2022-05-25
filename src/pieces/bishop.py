from pygame.sprite import AbstractGroup

from pieces.piece import Piece


class Bishop(Piece):

    def __init__(self, row: int, col: int, is_white: bool, *groups: AbstractGroup) -> None:
        super().__init__(row, col, is_white, *groups)
        self.value = 'B'
