from pygame.sprite import AbstractGroup

from pieces.piece import Piece


class Pawn(Piece):
    """
    Class representing the Pawn piece
    """

    def __init__(self, row: int, col: int, is_white: bool, *groups: AbstractGroup) -> None:
        super().__init__(row, col, is_white, *groups)
