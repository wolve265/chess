from board.coord import Coord
from pieces.piece import Piece


class King(Piece):
    """
    Class representing the King piece
    """

    def update_moves(self) -> None:
        self.moves = {Coord(1, 0), Coord(1, 1), Coord(0, 1), Coord(-1, 1), Coord(-1, 0), Coord(-1, -1), Coord(0, -1), Coord(1, -1)}
        return super().update_moves()
