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
from pieces.captures import Captures, WhiteCaptures, BlackCaptures
from pieces.generator import Generator
from pieces.knight import Knight
from pieces.piece import Piece
from pieces.pawn import Pawn
from pieces.king import King
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
        self.setup_board()
        game.squares.add(self.squares)
        self.setup_pieces()
        game.pieces.add(self.pieces)
        self.perform_end_turn_calculations()

    def setup_board(self) -> None:
        """
        Setups all board groups and sprites
        """
        for i in range(Settings.ROW_NUM):
            self.rows.append(Row(i))
            self.cols.append(Col(i))
        for row_i in range(Settings.ROW_NUM):
            for col_i in range(Settings.COL_NUM):
                self.squares.append(Square(Coord(row_i, col_i), self.rows[row_i], self.cols[col_i]))

    def setup_pieces(self) -> None:
        """
        Setups all pieces
        """
        pieces_gen = Generator(self.rows, self.cols)
        self.pieces = pieces_gen.run()

    def draw(self, surface: Surface) -> List[Rect]:
        game.screen.fill(Settings.BACKGROUND_COLOR)
        for square in self.squares:
            square.draw(surface)
        for row, col in zip(self.rows, self.cols):
            row.draw(surface)
            col.draw(surface)
        return super().draw(surface)

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

    @dispatch(tuple)
    def get_piece(self, pos: tuple[int]) -> Piece | None:
        """
        Returns Piece object from pos
        """
        for piece in self.pieces:
            if piece.full_rect.collidepoint(pos):
                return piece
        return None

    @dispatch(Square)
    def get_piece(self, square: Square) -> Piece:
        """
        Returns Piece object of the same position as square
        """
        for piece in self.pieces:
            if piece.full_rect.colliderect(square.full_rect):
                return piece

    def get_defender_piece_en_passant(self, square: Square) -> Piece:
        """
        Returns defender Piece object during en passant
        """
        for square_temp in self.squares:
            for move in Pawn.directions[game.state.player.value]:
                if (square_temp.coord + move) == square.coord:
                    return self.get_piece(square_temp)

    def get_attackers(self, square: Square) -> list[Piece]:
        """
        Returns attackers (list of Pieces) of specified square
        """
        attackers = []
        capture_group_type = WhiteCaptures if game.state.player == Player.WHITE else BlackCaptures
        for capture_group in square.groups():
            if not isinstance(capture_group, capture_group_type):
                continue
            for sprite in capture_group:
                if not isinstance(sprite, Piece):
                    continue
                attackers.append(sprite)
        return attackers

    def actions(self, event: Event) -> None:
        if self.update_king_checkmate():
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
                self.set_next_action(Action.MOVE)
        elif game.state.action == Action.MOVE:
            # Change selected piece or ...
            if self.try_select_piece():
                pass
            # ... move selected piece or ...
            elif self.try_move_piece():
                self.set_next_action(Action.END_TURN)
            # .. capture selected piece or ...
            elif self.try_capture_piece():
                self.set_next_action(Action.END_TURN)
            # ... deselect piece
            elif self.try_deselect_piece():
                self.set_next_action(Action.SELECT)
        elif game.state.action == Action.END_TURN:
            # End turn
            self.set_next_action(Action.SELECT)
            self.perform_end_turn_calculations()
            game.end_player_turn()

    def set_next_action(self, action: Action) -> None:
        game.state.action = action
        gen_event(NEXT_ACTION)

    def perform_end_turn_calculations(self) -> None:
        """
        Performs all updates needed at the end of player turn
        """
        self.reset_squares()
        self.update_pieces_flags()
        self.update_possible_moves_and_captures()
        self.update_checked_squares()
        self.update_king_check()
        self.update_king_checkmate()
        if game.state.check:
            self.update_possible_moves_and_captures_after_check()
        self.update_kings_moves()

    def reset_squares(self) -> None:
        """
        Resets all Squares
        """
        for square in self.squares:
            square.turn_render_reset()

    def update_pieces_flags(self) -> None:
        """
        Updates pieces flags of all Pieces
        """
        for piece in self.pieces:
            piece.update_flags()

    def update_possible_moves_and_captures(self) -> None:
        """
        Updates possible moves and captures of all Pieces
        """
        for piece in self.pieces:
            piece.update_possible_moves_and_captures()

    def update_possible_moves_and_captures_after_check(self) -> None:
        """
        Updates possible moves and captures of all Pieces after Check
        """
        for piece in self.pieces:
            piece.update_possible_moves_and_captures_after_check()

    def update_kings_moves(self) -> None:
        """
        Updates possible moves of Kings.
        Used after update_checked_squares to remove checked squares from moves.
        """
        for piece in self.pieces:
            if isinstance(piece, King):
                piece.update_possible_moves_and_captures()

    def update_checked_squares(self) -> None:
        """
        Updates checked flag of all Squares
        """
        for square in self.squares:
            square.checked_by.clear()
            for group in square.groups():
                if not isinstance(group, Captures):
                    continue
                if isinstance(group, WhiteCaptures):
                    square.checked_by.add(Player.WHITE)
                elif isinstance(group, BlackCaptures):
                    square.checked_by.add(Player.BLACK)

    def update_king_check(self) -> None:
        """
        Updates check flag according to current board state
        """
        game.state.check = False
        game.king_attackers.empty()
        game.is_knight_king_attacker = False
        for piece in self.pieces:
            if isinstance(piece, King):
                king = piece
                king_square = self.get_square(king)
                if king.player == game.state.player:
                    # Can't check own King
                    continue
                king_square.king_checked = False
                if game.state.player in king_square.checked_by:
                    king_square.king_checked = True
                    game.state.check = True
                    attackers = self.get_attackers(king_square)
                    game.is_knight_king_attacker = any([isinstance(atk, Knight) for atk in attackers])
                    game.king_attackers.add(*attackers)

    def update_king_checkmate(self) -> None:
        """
        Updates checkmate flag according to current board state
        """
        # TODO: Implement checkmate functionality
        return False

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
            if self.piece_pressed == self.piece_selected:
                return False
            for square in self.squares:
                square.render_reset()

        self.piece_selected = self.piece_pressed
        self.get_square(self.piece_selected).render_selection()
        for square in self.piece_selected.possible_moves:
            if not isinstance(square, Square):
                continue
            square.render_possible_move()
        for square in self.piece_selected.possible_captures:
            if not isinstance(square, Square):
                continue
            if piece := self.get_piece(square):
                if piece.player != self.piece_selected.player:
                    square.render_possible_capture()
            elif isinstance(self.piece_selected, Pawn):
                if self.piece_selected.can_en_passant:
                    self.piece_selected.en_passant_square.render_possible_capture()
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

        for square in self.squares:
            square.render_reset()

        # Pawns En Passant
        if isinstance(self.piece_selected, Pawn) and self.piece_selected.can_en_passant:
            for pawn_capture_square in self.piece_selected.capture_square_generator():
                if pawn_capture_square.coord == self.square_pressed.coord:
                    self.en_passant(self.piece_selected, self.square_pressed)
                    return True
        # Move a piece to an empty square
        self.move_piece(self.piece_selected, self.square_pressed)
        return True

    def try_capture_piece(self) -> bool:
        """
        Tries to capture a piece. If successful, returns True
        """
        # Cannot capture if no piece is pressed
        if self.piece_pressed is None:
            return False

        # Cannot capture if square is not in possible captures
        if not self.square_pressed in self.piece_selected.possible_captures:
            return False

        for square in self.squares:
            square.render_reset()

        self.capture_piece(self.piece_selected, self.piece_pressed)
        return True

    def try_deselect_piece(self) -> bool:
        """
        Tries to deselect a piece. If successful, returns True
        """
        if (self.square_pressed and self.piece_pressed is None) or \
           (self.piece_pressed is not None and self.piece_pressed == self.piece_selected):
            self.piece_selected = None
            for square in self.squares:
                square.render_reset()
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
        self.remove_piece(defender)

    def en_passant(self, attacker: Piece, square: Square) -> None:
        """
        Performs an en passant
        """
        defender = self.get_defender_piece_en_passant(square)
        attacker.move(square)
        self.remove_piece(defender)

    def remove_piece(self, piece: Piece) -> None:
        """
        Removes Piece from board
        """
        game.pieces.remove(piece)
        self.pieces.remove(piece)
        piece.possible_moves.empty()
        piece.possible_captures.empty()
        piece.kill()
