from board.coord import Coord
from pieces.piece import Piece


class Knight(Piece):
    """
    Class representing the Knight piece
    """

    move_range = 1
    directions = {Coord(2, 1), Coord(1, 2), Coord(-1, 2), Coord(-2, 1), Coord(-2, -1), Coord(-1, -2), Coord(1, -2), Coord(2, -1)}
