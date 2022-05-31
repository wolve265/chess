from board.coord import Coord
from pieces.piece import Piece
from settings import Settings


class Rook(Piece):
    """
    Class representing the Rook piece
    """

    move_range = 8
    directions = {Coord(1, 0), Coord(0, 1), Coord(-1, 0), Coord(0, -1)}
