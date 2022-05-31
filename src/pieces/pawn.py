from board.coord import Coord
from board.square import Square
from pieces.piece import Piece


class Pawn(Piece):
    """
    Class representing the Pawn piece
    """

    def update_moves(self) -> None:
        self.moves = {Coord(1, 0)} if self.moved else {Coord(1, 0), Coord(2, 0)}
        self.moves = set([move if self.is_white else move * Coord(-1, 1) for move in self.moves])
        return super().update_moves()

    def move(self, square: Square) -> None:
        self.moved = True
        self.update_moves()
        return super().move(square)
