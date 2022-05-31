from board.coord import Coord
from pieces.piece import Piece
from settings import Settings



class Queen(Piece):
    """
    Class representing the Queen piece
    """

    def update_moves(self) -> None:
        moves = set()
        # Bishop moves
        for mul in [Coord(1, 1), Coord(-1, 1), Coord(1, -1), Coord(-1, -1)]:
            for i in range(Settings.ROW_NUM):
                moves.add(Coord(i, i) * mul)
        # Rook moves
        for mul in [Coord(1, 1), Coord(-1, -1)]:
            for i in range(Settings.ROW_NUM):
                moves.add(Coord(i, 0) * mul)
                moves.add(Coord(0, i) * mul)
        self.moves = moves
        return super().update_moves()
