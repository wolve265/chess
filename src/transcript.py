from dataclasses import dataclass, field

import utils
from board.square import Square
from game import game
from pieces.piece import Piece


@dataclass
class GameMove:
    piece: Piece = field()
    destination: Square = field()
    promotion_piece: Piece | None = field(default=None)
    notation: str = field(init=False)

    def __post_init__(self) -> None:
        self.update_notation()

    def update_notation(self) -> None:
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
            if game.state.capture:
                if self.destination not in piece.captures:
                    continue
            else:
                if self.destination not in piece.legal_moves:
                    continue
            if piece.coord.col_i == self.piece.coord.col_i:
                ambiguous_col |= True
            else:
                ambiguous_row |= True
        return ambiguous_row, ambiguous_col

    def algebraic_notation(self, src_coord: str = "") -> str:
        if game.state.long_castle:
            return "O-O-O"
        if game.state.short_castle:
            return "O-O"
        capture_sign = "x" if game.state.capture else ""
        check_sign = "+" if game.state.check else ""
        checkmate_sign = "#" if game.state.checkmate else ""
        promotion_sign = self.promotion_piece.id if self.promotion_piece is not None else ""
        return (
            f"{self.piece.id}{src_coord}{capture_sign}{self.destination.coord}"
            f"{check_sign}{checkmate_sign}{promotion_sign}"
        )

    def long_algebraic_notation(self, ambiguous_row: bool, ambiguous_col: bool) -> str:
        col = utils.col_int2str(self.piece.coord.col_i) if ambiguous_row else ""
        row = utils.row_int2str(self.piece.coord.row_i) if ambiguous_col else ""
        src_coord = f"{col}{row}"
        return self.algebraic_notation(src_coord)
