from board.coord import Coord
from pieces.piece import Piece


class Bishop(Piece):
    """
    Class representing the Bishop piece
    """

    move_range = 8
    directions = {Coord(1, 1), Coord(-1, 1), Coord(-1, -1), Coord(1, -1)}
