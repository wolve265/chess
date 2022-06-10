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

    def __init__(self, coord: Coord, is_white: bool, *groups: AbstractGroup) -> None:
        super().__init__(coord, is_white, *groups)
        self.directions = self.directions[is_white]
        self.capture_directions =self.capture_directions[is_white]
        self.pawn = True

    def move(self, square: Square) -> None:
        self.move_range = 1
        return super().move(square)

    def update_possible_moves(self) -> None:
        super().update_possible_moves()

        for move in self.capture_directions:
            for square in game.squares:
                if (self.coord + move) != square.coord:
                    continue
                for piece in game.pieces:
                    if (self.coord + move) == piece.coord:
                        self.possible_moves.add(square)
