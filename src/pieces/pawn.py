from pygame.sprite import AbstractGroup

from board.coord import Coord
from board.square import Square
from game import *
from pieces.piece import Piece


class Pawn(Piece):
    """
    Class representing the Pawn piece
    """

    move_range = 2
    start_rows = {0 : 7, 1: 0}
    promotion_rows = {0 : 0, 1: 7}
    directions = {0 : {Coord(-1, 0)}, 1 : {Coord(1, 0)}}
    capture_directions = {0 : {Coord(-1, -1), Coord(-1, 1)}, 1 : {Coord(1, -1), Coord(1, 1)}}
    en_passant_directions = {0 : {Coord(0, -1), Coord(0, 1)}, 1 : {Coord(0, -1), Coord(0, 1)}}
    double_direction = {0 : Coord(-2, 0), 1 : Coord(2, 0)}

    def __init__(self, coord: Coord, is_white: bool, *groups: AbstractGroup) -> None:
        super().__init__(coord, is_white, *groups)
        self.id = ""
        self.start_row = self.start_rows[is_white]
        self.promotion_row = self.promotion_rows[is_white]
        self.directions = self.directions[is_white]
        self.capture_directions = self.capture_directions[is_white]
        self.double_direction = self.double_direction[is_white]
        self.en_passant_directions = self.en_passant_directions[is_white]
        self.en_passant_square: Square = None

        # Flags
        self.double_moved   = False
        self.can_en_passant = False

        # Counters
        self.double_moved_turn   = 0
        self.can_en_passant_turn = 0

    def move(self, square: Square) -> None:
        """
        Extends super implementation by
        marking the Pawn if double moved.
        """
        self.move_range = 1
        if (self.coord + self.double_direction) == square.coord:
            self.double_moved = True
            self.double_moved_turn = game.counter
        return super().move(square)

    def update_captures(self) -> None:
        """
        Overrides super class implementation.
        Updates captures according to Pawn capture_square_generator
        """
        for square in self.capture_square_generator():
            self.captures.add(square)

        # En Passant Captures
        for capture_move, en_passant_move in zip(self.capture_directions, self.en_passant_directions):
            if self.pinned and capture_move != self.pinned_direction:
                continue
            for square in game.squares:
                if not isinstance(square, Square):
                    continue
                if (self.coord + capture_move) != square.coord:
                    continue
                for piece in game.pieces:
                    if not isinstance(piece, Pawn):
                        continue
                    if ((self.coord + en_passant_move) == piece.coord
                        and piece.double_moved
                        and piece.player == self.player.opponent()):
                        self.can_en_passant = True
                        self.can_en_passant_turn = game.counter
                        self.en_passant_square = square
                        self.captures.add(square)

    def update_defended_squares(self) -> None:
        """
        Overrides super class implementation.
        Updates defended squares according to Pawn capture_square_generator
        """
        for square in self.capture_square_generator():
            self.defended_squares.add(square)

    def update_flags(self) -> None:
        """
        Extends super implementation by
        updating the Pawn flags
        """
        super().update_flags()
        if game.counter - self.can_en_passant_turn > 0:
            self.can_en_passant = False
        if game.counter - self.double_moved_turn > 0:
            self.double_moved = False

    def capture_square_generator(self) -> Square:
        """
        Generator for Pawn captures
        """
        for capture_move in self.capture_directions:
            if self.pinned and capture_move != self.pinned_direction:
                continue
            for square in game.squares:
                if not isinstance(square, Square):
                    continue
                if (self.coord + capture_move) == square.coord:
                    yield square
