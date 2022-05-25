from typing import *

from board.col import Col
from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.piece import Piece
from pieces.queen import Queen
from pieces.rook import Rook
from board.row import Row
from settings import Settings


class Generator:
    """
    Class used for generating chess pieces
    """

    def __init__(self, rows: List[Row], cols: List[Col]) -> None:
        self.rows = rows
        self.cols = cols

    def run(self) -> List[Piece]:
        pieces: List[Piece] = []

        # Pawns
        for row_i, is_white in zip((1,6), (True, False)):
            for col_i in range(Settings.cols):
                pieces.append(Pawn(row_i, col_i, is_white, self.rows[row_i], self.cols[col_i]))

        # Rooks, Knights, Bishops, Queens, Kings
        for row_i, is_white in zip((0,7), (True, False)):
            for col_i in (0, 7):
                pieces.append(Rook(row_i, col_i, is_white, self.rows[row_i], self.cols[col_i]))
            for col_i in (1, 6):
                pieces.append(Knight(row_i, col_i, is_white, self.rows[row_i], self.cols[col_i]))
            for col_i in (2, 5):
                pieces.append(Bishop(row_i, col_i, is_white, self.rows[row_i], self.cols[col_i]))
            col_i = 3
            pieces.append(Queen(row_i, col_i, is_white, self.rows[row_i], self.cols[col_i]))
            col_i = 4
            pieces.append(King(row_i, col_i, is_white, self.rows[row_i], self.cols[col_i]))
