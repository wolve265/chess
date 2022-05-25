from pygame.sprite import AbstractGroup

from pieces.piece import Piece


class Bishop(Piece):
    """
    Class representing the Bishop piece
    """

    def __init__(self, row: int, col: int, is_white: bool, *groups: AbstractGroup) -> None:
        super().__init__(row, col, is_white, *groups)
