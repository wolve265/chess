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
            for move in self.move_generator(direction):
                for square in game.squares:
                    if isinstance(square, Square) and (self.coord + move) != square.coord:
                        continue
                    if self.player.opponent() in square.checked_by:
                        continue
                    for piece in game.pieces:
                        if isinstance(piece, Piece) and (self.coord + move) == piece.coord:
                            self.possible_moves.add(square)
                            break
                    else:
                        self.possible_moves.add(square)
                        continue
                    break
                else:
                    continue
                break

    def move(self, square: Square) -> None:
        self.moved = True
        return super().move(square)
