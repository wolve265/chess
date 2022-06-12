from numpy import isin
import pygame

from multipledispatch import dispatch
from pygame.event import Event
from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface
from typing import *

from board.col import Col
from board.row import Row
from board.coord import Coord
from board.square import Square
from events import *
from game import *
from pieces.generator import Generator
from pieces.piece import Piece
from pieces.pawn import Pawn
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
        game.squares.add(self.squares)
        self.gen_pieces()
        game.pieces.add(self.pieces)
        self.update_possible_moves()

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
            self.update_possible_moves()
            game.state.action = Action.SELECT
            game.end_player_turn()

    def draw(self, surface: Surface) -> List[Rect]:
        game.screen.fill(Settings.BACKGROUND_COLOR)
        for square in self.squares:
            square.draw(surface)
        for row, col in zip(self.rows, self.cols):
            row.draw(surface)
            col.draw(surface)
        return super().draw(surface)

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)

    def update_possible_moves(self) -> None:
        for piece in self.pieces:
            piece.update_possible_moves()

    def gen_board(self) -> None:
        """
        Generates all board groups and sprites
        """
        for i in range(Settings.ROW_NUM):
            self.rows.append(Row(i))
            self.cols.append(Col(i))
        for row_i in range(Settings.ROW_NUM):
            for col_i in range(Settings.COL_NUM):
                self.squares.append(Square(Coord(row_i, col_i), self.rows[row_i], self.cols[col_i]))

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

    def get_all_squares(self) -> Sequence[Square]:
        """
        Gets all Square objects from Board sprites
        """
        return [sprite for sprite in self.sprites() if type(sprite) is Square]

    @dispatch(tuple)
    def get_square(self, pos: tuple[int]) -> Square | None:
        """
        Returns Square object from pos
        """
        for square in self.get_all_squares():
            if square.full_rect.collidepoint(pos):
                return square
        return None

    @dispatch(Piece)
    def get_square(self, piece: Piece) -> Square:
        """
        Returns Square object of the same position as piece
        """
        for square in self.get_all_squares():
            if square.full_rect.colliderect(piece.full_rect):
                return square

    def get_all_pieces(self) -> Sequence[Piece]:
        """
        Gets all Piece objects from Board sprites
        """
        return [sprite for sprite in self.sprites() if isinstance(sprite, Piece)]

    @dispatch(tuple)
    def get_piece(self, pos: tuple[int]) -> Piece | None:
        """
        Returns Piece object from pos
        """
        for piece in self.get_all_pieces():
            if piece.full_rect.collidepoint(pos):
                return piece
        return None

    @dispatch(Square)
    def get_piece(self, square: Square) -> Piece:
        """
        Returns Piece object of the same position as square
        """
        for piece in self.get_all_pieces():
            if piece.full_rect.colliderect(square.full_rect):
                return piece

    def get_defender_piece_en_passant(self, square: Square) -> Piece:
        """
        Returns defender Piece object during en passant
        """
        for square_temp in self.get_all_squares():
            for move in Pawn.directions[game.state.player.value]:
                if (square_temp.coord + move) == square.coord:
                    return self.get_piece(square_temp)

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
            for square in self.get_all_squares():
                square.render_reset()

        self.piece_selected = self.piece_pressed
        self.get_square(self.piece_selected).render_selection()
        for square in self.piece_selected.possible_moves:
            if not isinstance(square, Square):
                continue
            if piece := self.get_piece(square):
                if piece.player != self.piece_selected.player:
                    square.render_possible_capture()
            else:
                square.render_possible_move()
        return True

    def try_move_piece(self) -> bool:
        """
        Tries to move a piece. If successful, returns True
        """
        # Cannot move if no square is pressed
        if self.square_pressed is None:
            return False

        # Cannot move if square is not in possible moves
        if not self.square_pressed in self.piece_selected.possible_moves:
            return False

        for square in self.get_all_squares():
            square.render_reset()

        if self.piece_pressed is None:
            # Pawns En Passant
            if isinstance(self.piece_selected, Pawn) and self.piece_selected.can_en_passant:
                self.en_passant(self.piece_selected, self.square_pressed)
            # Move a piece to an empty square
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
        attacker.move(defender)
        game.pieces.remove(defender)
        self.remove_piece(defender)

    def en_passant(self, attacker: Piece, square: Square) -> None:
        """
        Performs an en passant
        """
        defender = self.get_defender_piece_en_passant(square)
        attacker.move(square)
        game.pieces.remove(defender)
        self.remove_piece(defender)

    def remove_piece(self, piece: Piece) -> None:
        """
        Removes Piece from board
        """
        piece.kill()
        piece.possible_moves.empty()
