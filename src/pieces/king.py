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

        # Flags
        self.moved = False

    def update_possible_moves(self) -> None:
        """
        Overrides super class implementation.
        King can't move to the defended square.
        """
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

        # Remove X-Ray attacker vision
        for attacker in game.king_attackers:
            attacker : Piece
            for direction in attacker.directions:
                for square in attacker.move_square_generator(direction):
                    if square in self.possible_moves:
                        self.possible_moves.remove(square)

    def update_possible_captures(self) -> None:
        """
        Overrides super class implementation.
        King can't capture the defended piece.
        """
        self.possible_captures.empty()

        for direction in self.directions:
            for square in self.move_square_generator(direction):
                if self.player.opponent() in square.checked_by:
                    continue
                for piece in game.pieces:
                    if not isinstance(piece, Piece):
                        continue
                    if square.coord == piece.coord:
                        self.possible_captures.add(square)
                        break
                else:
                    self.possible_captures.add(square)
                    continue
                break

    def move(self, square: Square) -> None:
        """
        Extends super implementation by
        marking the King if moved.
        """
        self.moved = True
        return super().move(square)
