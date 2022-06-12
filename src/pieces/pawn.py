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
    directions = {0 : {Coord(-1, 0)}, 1 : {Coord(1, 0)}}
    capture_directions = {0 : {Coord(-1, -1), Coord(-1, 1)}, 1 : {Coord(1, -1), Coord(1, 1)}}
    en_passant_directions = {0 : {Coord(0, -1), Coord(0, 1)}, 1 : {Coord(0, -1), Coord(0, 1)}}
    double_direction = {0 : Coord(-2, 0), 1 : Coord(2, 0)}

    def __init__(self, coord: Coord, is_white: bool, *groups: AbstractGroup) -> None:
        super().__init__(coord, is_white, *groups)
        self.directions = self.directions[is_white]
        self.capture_directions = self.capture_directions[is_white]
        self.double_direction = self.double_direction[is_white]
        self.en_passant_directions = self.en_passant_directions[is_white]
        self.double_moved   = False
        self.can_en_passant = False
        self.double_moved_turn   = 0
        self.can_en_passant_turn = 0

    def move(self, square: Square) -> None:
        self.move_range = 1
        if (self.coord + self.double_direction) == square.coord:
            self.double_moved = True
            self.double_moved_turn = game.turn_counter
        return super().move(square)

    def update_possible_moves(self) -> None:
        self.possible_moves.empty()

        # Basic moves
        for direction in self.directions:
            for move in self.move_generator(direction):
                for square in game.squares:
                    if isinstance(square, Square) and (self.coord + move) != square.coord:
                        continue
                    for piece in game.pieces:
                        if isinstance(piece, Piece) and (self.coord + move) == piece.coord:
                            break
                    else:
                        self.possible_moves.add(square)
                        continue
                    break
                else:
                    continue
                break

        # Capture moves
        for capture_move, en_passant_move in zip(self.capture_directions, self.en_passant_directions):
            for square in game.squares:
                if isinstance(square, Square) and (self.coord + capture_move) != square.coord:
                    continue
                for piece in game.pieces:
                    if isinstance(piece, Piece) and (self.coord + capture_move) == piece.coord:
                        self.possible_moves.add(square)
                    elif isinstance(piece, Pawn) and (self.coord + en_passant_move) == piece.coord and piece.double_moved:
                        self.can_en_passant = True
                        self.can_en_passant_turn = game.turn_counter
                        self.possible_moves.add(square)

    def update_flags(self) -> None:
        if game.turn_counter - self.can_en_passant_turn > 1:
            self.can_en_passant = False
        if game.turn_counter - self.double_moved_turn > 1:
            self.double_moved = False
        return super().update_flags()

    def capture_square_generator(self) -> Square:
        for capture_move in self.capture_directions:
            for square in game.squares:
                if isinstance(square, Square) and (self.coord + capture_move) == square.coord:
                    yield square
