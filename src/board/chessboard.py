import pygame

from multipledispatch import dispatch
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
        self.square_pressed: Square = None
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
        self.square_pressed = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                self.piece_pressed = self.get_piece(event.pos)
                self.square_pressed = self.get_square(event.pos)

        # Actions "State Machine"
        if game.state.action == Action.SELECT:
            # Select a piece
            if self.try_select_piece():
                game.state.action = Action.MOVE
        elif game.state.action == Action.MOVE:
            # Change selected piece or ...
            if self.try_select_piece():
                pass
            # ... move selected piece
            elif self.try_move_piece():
                game.state.action = Action.END_TURN
        elif game.state.action == Action.END_TURN:
            # End turn
            game.state.action = Action.SELECT
            game.end_player_turn()

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
        Returns True if there is a checkmate
        """
        # TODO: Implement checkmate functionality
        return False

    @dispatch(tuple)
    def get_square(self, pos: tuple[int]) -> Square | None:
        """
        Returns Square object from pos
        """
        for square in self.squares:
            if square.full_rect.collidepoint(pos):
                return square
        return None

    @dispatch(Piece)
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

    def try_select_piece(self) -> bool:
        """
        Tries to select a piece. If successful, returns True
        """
        if self.piece_pressed is None:
            # Can only select pieces
            return False
        if self.piece_pressed.player != game.state.player:
            # Can only select own pieces
            return False
        if self.piece_selected is not None:
            self.get_square(self.piece_selected).deselect()
        self.piece_selected = self.piece_pressed
        self.get_square(self.piece_selected).select()
        return True

    def try_move_piece(self) -> bool:
        """
        Tries to move a piece. If successful, returns True
        """
        # Can move a piece to an empty square as well as to another piece
        if self.square_pressed is None:
            return False
        self.get_square(self.piece_selected).deselect()

        # Move a piece to an empty square
        if self.piece_pressed is None:
            self.move_piece(self.piece_selected, self.square_pressed)
            return True

        # Move a piece to another piece = perform a capture
        self.capture_piece(self.piece_selected, self.piece_pressed)
        return True

    def move_piece(self, piece: Piece, square: Square) -> None:
        """
        Moves a Piece to desired Square
        """
        piece.move(square)

    def capture_piece(self, attacker: Piece, defender: Piece) -> None:
        """
        Attacker Piece captures the defender Piece
        """
        self.pieces.remove(defender)
        defender.kill()
        attacker.move(defender)
