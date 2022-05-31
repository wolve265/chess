from board.coord import Coord
from pieces.piece import Piece
from settings import Settings


class Bishop(Piece):
    """
    Class representing the Bishop piece
    """

    def update_moves(self) -> None:
        moves = set()
        for mul in [Coord(1, 1), Coord(-1, 1), Coord(1, -1), Coord(-1, -1)]:
            for i in range(Settings.ROW_NUM):
                moves.add(Coord(i, i) * mul)
        self.moves = moves
        return super().update_moves()
