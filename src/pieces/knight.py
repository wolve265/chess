from board.coord import Coord
from pieces.piece import Piece


class Knight(Piece):
    """
    Class representing the Knight piece
    """

    def update_moves(self) -> None:
        self.moves = {Coord(2, 1), Coord(1, 2), Coord(-1, 2), Coord(-2, 1), Coord(-2, -1), Coord(-1, -2), Coord(1, -2), Coord(2, -1)}
        return super().update_moves()
