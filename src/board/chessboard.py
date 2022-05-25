from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface
from typing import *

from board.col import Col
from board.row import Row
from board.square import Square
from game import game
from pieces.generator import Generator
from pieces.piece import Piece
from settings import Settings


class Board(Group):

    def __init__(self, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        self.squares: List[Square] = []
        self.pieces: List[Piece] = []
        self.rows: List[Row] = []
        self.cols: List[Col] = []
        self.gen_board()
        self.gen_pieces()
        super().__init__(self.squares, self.pieces, *sprites)

    def draw(self, surface: Surface) -> List[Rect]:
        game.screen.fill(Settings.background_color)
        for square in self.squares:
            square.draw(surface)
        for row, col in zip(self.rows, self.cols):
            row.draw(surface)
            col.draw(surface)
        return super().draw(surface)

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)

    def gen_board(self) -> None:
        for i in range(Settings.rows):
            self.rows.append(Row(i))
            self.cols.append(Col(i))
        for row_i in range(Settings.rows):
            for col_i in range(Settings.cols):
                self.squares.append(Square(row_i, col_i, self.rows[row_i], self.cols[col_i]))

    def gen_pieces(self) -> None:
        pieces_gen = Generator(self.rows, self.cols)
        self.pieces = pieces_gen.run()
