from pygame.sprite import AbstractGroup

from pieces.piece import Piece


class Pawn(Piece):

    def __init__(self, row: int, col: int, is_white: bool, *groups: AbstractGroup) -> None:
        self.value = 'P'
        super().__init__(row, col, is_white, *groups)
