from pygame.sprite import AbstractGroup

from board.coord import Coord
from board.square import Square
from pieces.piece import Piece


class Pawn(Piece):
    """
    Class representing the Pawn piece
    """

    move_range = 2
    directions = {Coord(1, 0)}

    def __init__(self, coord: Coord, is_white: bool, *groups: AbstractGroup) -> None:
        self.directions = self.directions if is_white else {Coord(-1, 0)}
        super().__init__(coord, is_white, *groups)

    def move(self, square: Square) -> None:
        self.move_range = 1
        self.update_moves()
        return super().move(square)
