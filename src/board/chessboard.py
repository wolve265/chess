import pygame

from pygame.event import Event
from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface
from typing import Optional, Sequence, Type, Union

from board.col import Col
from board.row import Row
from board.coord import Coord
from board.square import Square
from events import *
from game import *
from pieces.bishop import Bishop
from pieces.moves import WhiteCaptures, BlackCaptures, WhiteDefendedSquares, BlackDefendedSquares
from pieces.generator import Generator
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.piece import Piece
from pieces.queen import Queen
from pieces.rook import Rook
from settings import Settings
from transcript import GameMove


class Board(Group):
    """
    Class representing the chessboard
    """

    def __init__(self, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        self.squares: list[Square] = []
        self.pieces: list[Piece] = []
        self.rows: list[Row] = []
        self.cols: list[Col] = []
        self.square_pressed: Optional[Square] = None
        self.square_selected: Optional[Square] = None
        self.piece_pressed: Optional[Piece] = None
        self.piece_selected: Optional[Piece] = None
        self.current_game_move: Optional[GameMove] = None
        self.transcript: list[GameMove] = []
        self.setup()
        super().__init__(self.squares, self.pieces, *sprites)

    def setup(self) -> None:
        """
        Sets all up
        """
        self.setup_board()

        game.squares.add(self.squares)
        game.pieces.add(self.pieces)
        for piece in self.pieces:
            piece.setup()

        game.setup()

    def setup_board(self) -> None:
        """
        Sets up all board groups and sprites
        """
        # Generate Rows and Cols
        for i in range(Settings.ROW_NUM):
            self.rows.append(Row(i))
            self.cols.append(Col(i))
        # Generate Squares
        for row_i in range(Settings.ROW_NUM):
            for col_i in range(Settings.COL_NUM):
                self.squares.append(Square(Coord(row_i, col_i), self.rows[row_i], self.cols[col_i]))
        # Generate Pieces
        pieces_gen = Generator(self.rows, self.cols)
        self.pieces = pieces_gen.run()

    def draw(self, surface: Surface) -> list[Rect]:
        game.screen.fill(Settings.BACKGROUND_COLOR)
        for square in self.squares:
            square.draw(surface)
        for row, col in zip(self.rows, self.cols):
            row.draw(surface)
            col.draw(surface)
        return super().draw(surface)

    def get_square(self, obj: tuple[int, int] | Coord | Piece) -> Square | None:
        """
        Returns Square object from pos or coord or piece
        """
        for square in self.squares:
            if isinstance(obj, tuple):
                if square.full_rect.collidepoint(obj):
                    return square
            elif isinstance(obj, Coord):
                if square.coord == obj:
                    return square
            else:
                if square.coord == obj.coord:
                    return square
        return None


    def get_piece(self, obj: tuple[int, int] | Coord | Square) -> Piece | None:
        """
        Returns Piece object from pos
        """
        for piece in self.pieces:
            if isinstance(obj, tuple):
                if piece.full_rect.collidepoint(obj):
                    return piece
            elif isinstance(obj, Coord):
                if piece.coord == obj:
                    return piece
            else:
                if piece.coord == obj.coord:
                    return piece
        return None

    def get_defender_piece_en_passant(self, square: Square) -> Piece:
        """
        Returns defender Piece object during en passant
        """
        for square_temp in self.squares:
            for move in Pawn.pawn_directions_dict[game.state.player.value]:
                if (square_temp.coord + move) == square.coord:
                    piece = self.get_piece(square_temp)
                    if piece:
                        return piece
        raise Exception("Impossible! Cannot find defender piece in en passant")

    def get_attackers(self, square: Square) -> list[Piece]:
        """
        Returns attackers (list of Pieces) of specified square
        """
        attackers: list[Piece] = []
        capture_group_type = WhiteCaptures if game.state.player == Player.WHITE else BlackCaptures
        for capture_group in square.groups():
            if not isinstance(capture_group, capture_group_type):
                continue
            if not isinstance(capture_group.owner.sprite, Piece):
                continue
            attackers.append(capture_group.owner.sprite)
        return attackers

    def get_squares_between_king_and_attacker(self, king: King, attacker: Piece) -> list[Square]:
        """
        Returns squares between king and attacker
        """
        squares: list[Square] = []
        # Can't block Knight attack
        if isinstance(attacker, Knight):
            return squares
        coord = king.coord - attacker.coord
        direction = coord.get_direction()
        for square in attacker.move_square_generator(direction):
            if self.get_piece(square):
                break
            squares.append(square)
        return squares

    def actions(self, event: Event) -> None:
        self.piece_pressed = None
        self.square_pressed = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                self.piece_pressed = self.get_piece(event.pos)
                self.square_pressed = self.get_square(event.pos)

        # Actions "State Machine"
        if game.state.action == Action.SELECT:
            game.update_at_start_turn()
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
            if game.state.checkmate or game.state.stalemate:
                gen_event(END_GAME)
            else:
                if self.current_game_move:
                    self.transcript.append(self.current_game_move)
                game.end_player_turn(self.current_game_move.notation)

    def set_next_action(self, action: Action) -> None:
        """
        Sets next action and generates dummy event.
        Waiting for users events are no longer required.
        """
        game.state.action = action
        gen_event(NEXT_ACTION)

    def perform_end_turn_calculations(self) -> None:
        """
        Performs all updates needed at the end of player turn
        """
        self.reset_squares()
        self.update_pieces_flags()
        self.update_pinned_pieces()
        self.update_possible_moves()
        self.update_defended_squares()
        self.update_king_check()
        self.current_game_move.update_notation()
        if game.state.check:
            self.update_squares_between_king_and_attacker()
            self.update_possible_moves_after_check()
        self.update_kings_moves()
        if not game.state.check:
            self.update_king_stalemate()
        if game.state.check:
            self.update_kings_moves_after_check()
            self.update_king_checkmate()

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

    def update_possible_moves(self) -> None:
        """
        Updates possible moves and captures of all Pieces
        """
        for piece in self.pieces:
            piece.update_moves()

    def update_possible_moves_after_check(self) -> None:
        """
        Updates possible moves and captures of all Pieces after Check
        """
        for piece in self.pieces:
            piece.update_moves_after_check()

    def update_kings_moves(self) -> None:
        """
        Updates possible moves of Kings.
        Used after update_checked_squares to remove checked squares from moves.
        """
        for piece in self.pieces:
            if isinstance(piece, King):
                piece.update_moves()

    def update_kings_moves_after_check(self) -> None:
        """
        Updates possible moves of King after check.
        Used after update_checked_squares to remove checked squares from moves.
        """
        for piece in self.pieces:
            if isinstance(piece, King):
                piece.update_moves_after_check()

    def update_defended_squares(self) -> None:
        """
        Updates defended_by flag of all Squares
        """
        for square in self.squares:
            square.defended_by.clear()
            for group in square.groups():
                if isinstance(group, WhiteDefendedSquares):
                    square.defended_by.add(Player.WHITE)
                elif isinstance(group, BlackDefendedSquares):
                    square.defended_by.add(Player.BLACK)

    def update_pinned_pieces(self) -> None:
        """
        Updates pinned flag of all Pieces
        """
        for piece in self.pieces:
            if piece.move_range < 8:
                continue
            for direction in piece.directions:
                piece1: Optional[Piece] = None
                piece2: Optional[Piece] = None
                for square in piece.move_square_generator(direction):
                    piece_target = self.get_piece(square)
                    if not piece_target:
                        continue
                    # Can't pin own Pieces
                    if piece.player == piece_target.player:
                        break
                    if piece1 is None:
                        piece1 = piece_target
                    else:
                        piece2 = piece_target
                        break
                if isinstance(piece2, King):
                    piece1.pinned_directions.add(direction)
                    piece1.pinned_directions.add(direction * Coord(-1, -1))
                    piece1.pinned = True

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
                if not king_square:
                    raise Exception("Impossible! Cannot find Square of King object")
                if king.player == game.state.player:
                    # Can't check own King
                    continue
                king_square.king_checked = False
                if game.state.player in king_square.defended_by:
                    king_square.king_checked = True
                    game.state.check = True
                    attackers = self.get_attackers(king_square)
                    game.is_knight_king_attacker = any([isinstance(atk, Knight) for atk in attackers])
                    game.king_attackers.add(*attackers)

    def update_squares_between_king_and_attacker(self) -> None:
        """
        Updates squares between king and attacker
        """
        game.squares_between_king_and_attacker.empty()
        king_attackers: list[Piece] = [sprite for sprite in game.king_attackers if isinstance(sprite, Piece)]
        if len(king_attackers) > 1:
            return
        attacker = king_attackers[0]
        king: Optional[King] = None
        for piece in self.pieces:
            if not isinstance(piece, King):
                continue
            if piece.player == game.state.player:
                continue
            king = piece
        if not king:
            return
        squares = self.get_squares_between_king_and_attacker(king, attacker)
        game.squares_between_king_and_attacker.add(*squares)

    def update_king_checkmate(self) -> None:
        """
        Sets checkmate flag according to current board state
        """
        game.state.checkmate = not self.opponent_has_legal_moves()

    def update_king_stalemate(self) -> None:
        """
        Sets stalemate flag according to current board state
        """
        game.state.stalemate = not self.opponent_has_legal_moves()

    def opponent_has_legal_moves(self) -> bool:
        """
        Returns True if opponent has legal moves. Otherwise returns False
        """
        for piece in self.pieces:
            if piece.player.opponent() == game.state.player:
                if len(piece.legal_moves) or len(piece.captures):
                    return True
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
        for square in self.piece_selected.legal_moves:
            if not isinstance(square, Square):
                continue
            square.render_possible_move()
        for square in self.piece_selected.captures:
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
        # Cannot move if no piece is selected
        if self.piece_selected is None:
            return False

        # Cannot move if no square is pressed
        if self.square_pressed is None:
            return False

        # Cannot move if square is not in legal moves
        if not self.square_pressed in self.piece_selected.legal_moves:
            return False

        for square in self.squares:
            square.render_reset()

        self.square_selected = self.square_pressed
        # Castling
        if isinstance(self.piece_selected, King):
            move = self.square_pressed.coord - self.piece_selected.coord
            if (move/move.get_direction()).col_i > King.move_range:
                direction = move.get_direction()
                self.castle(self.piece_selected, self.square_selected, direction)
                return True

        # Pawn promotion
        if isinstance(self.piece_selected, Pawn):
            if self.square_selected.get_row().row_i == self.piece_selected.promotion_row:
                self.promote_move(self.piece_selected, self.square_selected)
                return True

        # Move a piece to an empty square
        self.move_piece(self.piece_selected, self.square_selected)
        return True

    def try_capture_piece(self) -> bool:
        """
        Tries to capture a piece. If successful, returns True
        """
        # Cannot capture if no piece is selected
        if self.piece_selected is None:
            return False

        # Cannot capture if no square is pressed
        if self.square_pressed is None:
            return False

        # Cannot capture if no piece is pressed unless it's en passant
        if self.piece_pressed is None:
            return self.try_capture_en_passant()

        # Cannot capture if square is not in possible captures
        if not self.square_pressed in self.piece_selected.captures:
            return False

        for square in self.squares:
            square.render_reset()

        self.square_selected = self.square_pressed

        # Pawn promotion
        if isinstance(self.piece_selected, Pawn):
            if self.square_selected.get_row().row_i == self.piece_selected.promotion_row:
                self.promote_capture(self.piece_selected, self.piece_pressed)
                return True

        self.capture_piece(self.piece_selected, self.piece_pressed)
        return True

    def try_capture_en_passant(self) -> bool:
        """
        Tries to capture en passant. If successful, returns True
        """
        # Only Pawns can en passant
        if not isinstance(self.piece_selected, Pawn):
            return False

        # Square must be pressed
        if self.square_pressed is None:
            return False

        if self.piece_selected.can_en_passant:
            for pawn_capture in self.piece_selected.captures:
                if not isinstance(pawn_capture, Square):
                    continue
                if pawn_capture.coord == self.square_pressed.coord:
                    self.square_selected = self.square_pressed
                    self.en_passant(self.piece_selected, self.square_selected)
                    return True
        return False

    def try_deselect_piece(self) -> bool:
        """
        Tries to deselect a piece. If successful, returns True
        """
        if ((self.square_pressed and self.piece_pressed is None) or
           (self.piece_pressed is not None and self.piece_pressed == self.piece_selected)):
            self.piece_selected = None
            for square in self.squares:
                square.render_reset()
            return True
        return False

    def move_piece(self, piece: Piece, square: Square) -> None:
        """
        Moves a Piece to desired Square
        """
        self.current_game_move = GameMove(piece, square)
        piece.move(square)

    def castle(self, king: Piece, king_dst_square: Square, direction: Coord) -> None:
        """
        Castles
        """
        rook: Optional[Rook] = None
        rook_dst_square: Optional[Square] = None
        for sprite in king.get_row():
            if not isinstance(sprite, Rook):
                continue
            if (direction == Coord(0, 1) and sprite.coord > king.coord or
                direction == Coord(0, -1) and sprite.coord < king.coord):
                rook = sprite
                rook_dst_square = self.get_square(king.coord + direction)
        if abs((king.coord - rook.coord).col_i) > 3:
            game.state.long_castle = True
        else:
            game.state.short_castle = True
        if not rook_dst_square:
            raise Exception("Impossible! Cannot find rook destination square during castling")
        self.current_game_move = GameMove(king, king_dst_square)
        king.move(king_dst_square)
        rook.move(rook_dst_square)

    def get_user_promotion_type(self) -> Type[Piece]:
        possible_promotion = {
            "Q": Queen,
            "R": Rook,
            "B": Bishop,
            "N": Knight
        }
        ids = possible_promotion.keys()
        while (user_input := input(f"Choose from {[*ids]}")) not in ids: ...
        return possible_promotion[user_input]

    def promote_move(self, pawn: Pawn, square: Square) -> None:
        """
        Promotes Pawn by move
        """
        promotion_piece_type = self.get_user_promotion_type()
        promotion_piece = promotion_piece_type(pawn.coord, pawn.player.value, *pawn.groups())
        promotion_piece.setup()
        game.pieces.add(promotion_piece)
        self.pieces.append(promotion_piece)
        self.current_game_move = GameMove(pawn, square, promotion_piece)
        self.remove_piece(pawn)
        promotion_piece.move(square)

    def capture_piece(self, attacker: Piece, defender: Piece) -> None:
        """
        Attacker Piece captures the defender Piece
        """
        game.state.capture = True
        defender_square = self.get_square(defender)
        if not defender_square:
            raise Exception("Impossible! Cannot find Square of Piece object")
        self.current_game_move = GameMove(attacker, defender_square)
        attacker.move(defender)
        self.remove_piece(defender)

    def en_passant(self, attacker: Piece, square: Square) -> None:
        """
        Performs an En Passant
        """
        game.state.capture = True
        self.current_game_move = GameMove(attacker, square)
        defender = self.get_defender_piece_en_passant(square)
        attacker.move(square)
        self.remove_piece(defender)

    def promote_capture(self, pawn: Pawn, defender: Piece) -> None:
        """
        Promotes Pawn by capture
        """
        promotion_piece_type = self.get_user_promotion_type()
        promotion_piece = promotion_piece_type(pawn.coord, pawn.player.value, *pawn.groups())
        promotion_piece.setup()
        game.pieces.add(promotion_piece)
        self.pieces.append(promotion_piece)
        defender_square = self.get_square(defender)
        if not defender_square:
            raise Exception("Impossible! Cannot find Square of Piece object")
        self.current_game_move = GameMove(pawn, defender_square, promotion_piece)
        self.remove_piece(pawn)
        promotion_piece.move(defender)
        self.remove_piece(defender)

    def remove_piece(self, piece: Piece) -> None:
        """
        Removes Piece from board
        """
        game.pieces.remove(piece)
        self.pieces.remove(piece)
        piece.kill()
