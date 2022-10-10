from pygame.sprite import AbstractGroup

from board.coord import Coord
from board.square import Square
from pieces.piece import Piece


class Rook(Piece):
    """
    Class representing the Rook piece
    """

    move_range = 8
    directions = {Coord(1, 0), Coord(0, 1), Coord(-1, 0), Coord(0, -1)}

    def __init__(self, coord: Coord, is_white: bool, *groups: AbstractGroup) -> None:
        super().__init__(coord, is_white, *groups)

        # Flags
        self.moved = False

    def move(self, square: Square) -> None:
        """
        Extends super implementation by
        marking the Rook if moved.
        """
        self.moved = True
        return super().move(square)
