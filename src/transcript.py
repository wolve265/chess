from dataclasses import dataclass, field

from board.square import Square
from pieces.piece import Piece
from game import *
from utils import *

@dataclass
class GameMove:
    piece: Piece = field()
    destination: Square = field()
    state: State = field()
    promotion_piece: Piece = field(init=False)
    notation: str = field(init=False)

    def __post_init__(self) -> None:
        ambiguous_row, ambiguous_col = self.is_ambiguous()
        if any([ambiguous_row, ambiguous_col]):
            self.notation = self.long_algebraic_notation(ambiguous_row, ambiguous_col)
            return
        self.notation = self.algebraic_notation()

    def is_ambiguous(self) -> tuple[bool, bool]:
        ambiguous_row, ambiguous_col = False, False
        for piece in game.pieces:
            if not isinstance(piece, self.piece.__class__):
                continue
            if piece.coord == self.piece.coord:
                continue
            if piece.player != self.piece.player:
                continue
            if self.state.capture:
                if not self.destination in piece.captures:
                    continue
            else:
                if not self.destination in piece.legal_moves:
                    continue
            if piece.coord.col_i == self.piece.coord.col_i:
                ambiguous_col |= True
            else:
                ambiguous_row |= True
        return ambiguous_row, ambiguous_col

    def algebraic_notation(self, src_coord: str = "") -> str:
        if self.state.long_castle:
            return "O-O-O"
        if self.state.short_castle:
            return "O-O"
        capture_sign = "x" if self.state.capture else ""
        check_sign = "+" if self.state.check else ""
        checkmate_sign = "#" if self.state.checkmate else ""
        promotion_sign = self.promotion_piece.id if hasattr(self, "promotion_piece") else ""
        return f"{self.piece.id}{src_coord}{capture_sign}{self.destination.coord}{check_sign}{checkmate_sign}{promotion_sign}"

    def long_algebraic_notation(self, ambiguous_row: bool, ambiguous_col: bool) -> str:
        col = col_int2str(self.piece.coord.col_i) if ambiguous_row else ""
        row = row_int2str(self.piece.coord.row_i) if ambiguous_col else ""
        src_coord = f"{col}{row}"
        return self.algebraic_notation(src_coord)
