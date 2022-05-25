from typing import *

from col import Col
from pieces.piece import Piece
from pieces.pawn import Pawn
from row import Row
from settings import Settings


class Generator:
    """
    Use this class to generate chess pieces
    """

    def __init__(self, rows: List[Row], cols: List[Col]) -> None:
        self.rows = rows
        self.cols = cols

    def run(self) -> List[Piece]:
        pawns: List[Pawn] = []

        ## Pawns
        for row_i, is_white in zip((1,6), (True, False)):
            for col_i in range(Settings.cols):
                pawns.append(Pawn(row_i, col_i, is_white, self.rows[row_i], self.cols[col_i]))
