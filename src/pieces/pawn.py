from pygame.sprite import AbstractGroup

from board.coord import Coord
from board.square import Square
from game import *
from pieces.piece import Piece


class Pawn(Piece):
    """
    Class representing the Pawn piece
    """

    move_range = 2
    directions = {Coord(1, 0)}

    def __init__(self, coord: Coord, is_white: bool, *groups: AbstractGroup) -> None:
        super().__init__(coord, is_white, *groups)
        self.directions = self.directions if is_white else {Coord(-1, 0)}
        self.pawn = True

    def move(self, square: Square) -> None:
        self.move_range = 1
        return super().move(square)
