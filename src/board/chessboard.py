import pygame

from pygame.event import Event
from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface
from typing import *

from board.col import Col
from board.row import Row
from board.square import Square
from events import *
from game import *
from pieces.generator import Generator
from pieces.piece import Piece
from settings import Settings


class Board(Group):
    """
    Class representing the chessboard
    """

    def __init__(self, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        self.squares: List[Square] = []
        self.pieces: List[Piece] = []
        self.rows: List[Row] = []
        self.cols: List[Col] = []
        self.piece_pressed: Piece = None
        self.piece_selected: Piece = None
        self.setup()
        super().__init__(self.squares, self.pieces, *sprites)

    def setup(self) -> None:
        self.gen_board()
        self.gen_pieces()

    def actions(self, event: Event) -> None:
        if self.is_checkmate():
            gen_event(END_GAME)
            return

        self.piece_pressed = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                self.piece_pressed = self.get_piece(event.pos)

        if self.piece_pressed is not None:
            if game.state.action == Action.SELECT:
                game.state.action = Action.PLACE
                self.piece_selected = self.piece_pressed
                self.get_square(self.piece_selected).select()
            elif game.state.action == Action.PLACE:
                self.get_square(self.piece_selected).deselect()
                if self.piece_selected == self.piece_pressed:
                    game.state.action = Action.SELECT
                else:
                    pass

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
        """
        Generates all board groups and sprites
        """
        for i in range(Settings.rows):
            self.rows.append(Row(i))
            self.cols.append(Col(i))
        for row_i in range(Settings.rows):
            for col_i in range(Settings.cols):
                self.squares.append(Square(row_i, col_i, self.rows[row_i], self.cols[col_i]))

    def gen_pieces(self) -> None:
        """
        Generates all pieces
        """
        pieces_gen = Generator(self.rows, self.cols)
        self.pieces = pieces_gen.run()

    def is_checkmate(self) -> bool:
        """
        Returns information if there is a checkmate
        """
        # TODO: Implement checkmate functionality
        return False

    def get_square(self, pos: tuple[int]) -> Square | None:
        """
        Returns Square object from pos
        """
        for square in self.squares:
            if square.full_rect.collidepoint(pos):
                return square
        return None

    def get_square(self, piece: Piece) -> Square:
        """
        Returns Square object of the same position as piece
        """
        for square in self.squares:
            if square.full_rect.colliderect(piece.full_rect):
                return square

    def get_piece(self, pos: tuple[int]) -> Piece | None:
        """
        Returns Piece object from pos
        """
        for piece in self.pieces:
            if piece.full_rect.collidepoint(pos):
                return piece
        return None
