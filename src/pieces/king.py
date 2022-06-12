from pygame.sprite import AbstractGroup

from board.coord import Coord
from board.square import Square
from game import *
from pieces.piece import Piece


class King(Piece):
    """
    Class representing the King piece
    """

    move_range = 1
    directions = {Coord(1, 0), Coord(1, 1), Coord(0, 1), Coord(-1, 1), Coord(-1, 0), Coord(-1, -1), Coord(0, -1), Coord(1, -1)}

    def __init__(self, coord: Coord, is_white: bool, *groups: AbstractGroup) -> None:
        super().__init__(coord, is_white, *groups)
        self.moved = False

    def update_possible_moves(self) -> None:
        self.possible_moves.empty()

        for direction in self.directions:
            for square in self.move_square_generator(direction):
                if self.player.opponent() in square.checked_by:
                    continue
                for piece in game.pieces:
                    if not isinstance(piece, Piece):
                        continue
                    if square.coord == piece.coord:
                        break
                else:
                    self.possible_moves.add(square)
                    continue
                break

    def move(self, square: Square) -> None:
        self.moved = True
        return super().move(square)
