from board.coord import Coord
from pieces.piece import Piece


class Queen(Piece):
    """
    Class representing the Queen piece
    """

    move_range = 8
    directions = {Coord(1, 0), Coord(1, 1), Coord(0, 1), Coord(-1, 1), Coord(-1, 0), Coord(-1, -1), Coord(0, -1), Coord(1, -1)}
