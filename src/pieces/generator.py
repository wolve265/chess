from board.col import Col
from board.row import Row
from board.coord import Coord
from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.piece import Piece
from pieces.queen import Queen
from pieces.rook import Rook
from settings import Settings


class Generator:
    """
    Class used for generating chess pieces
    """

    def __init__(self, rows: list[Row], cols: list[Col]) -> None:
        self.rows = rows
        self.cols = cols

    def run(self) -> list[Piece]:
        pieces: list[Piece] = []

        # Pawns
        for row_i, is_white in zip((1,6), (True, False)):
            for col_i in range(Settings.COL_NUM):
                pieces.append(Pawn(Coord(row_i, col_i), is_white, self.rows[row_i], self.cols[col_i]))

        # Rooks, Knights, Bishops, Queens, Kings
        for row_i, is_white in zip((0,7), (True, False)):
            for col_i in (0, 7):
                pieces.append(Rook(Coord(row_i, col_i), is_white, self.rows[row_i], self.cols[col_i]))
            for col_i in (1, 6):
                pieces.append(Knight(Coord(row_i, col_i), is_white, self.rows[row_i], self.cols[col_i]))
            for col_i in (2, 5):
                pieces.append(Bishop(Coord(row_i, col_i), is_white, self.rows[row_i], self.cols[col_i]))
            col_i = 3
            pieces.append(Queen(Coord(row_i, col_i), is_white, self.rows[row_i], self.cols[col_i]))
            col_i = 4
            pieces.append(King(Coord(row_i, col_i), is_white, self.rows[row_i], self.cols[col_i]))

        return pieces
