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

    def update_legal_moves(self) -> None:
        """
        Overrides super class implementation.
        King can't move to the defended square.
        """
        for direction in self.directions:
            square: Square
            for square in self.move_square_generator(direction):
                if self.player.opponent() in square.defended_by:
                    continue
                piece: Piece
                for piece in game.pieces:
                    if square.coord == piece.coord:
                        break
                else:
                    self.legal_moves.add(square)

    def update_captures(self) -> None:
        """
        Overrides super class implementation.
        King can't capture the defended piece.
        """
        for direction in self.directions:
            square: Square
            for square in self.move_square_generator(direction):
                if self.player.opponent() in square.defended_by:
                    continue
                piece: Piece
                for piece in game.pieces:
                    if square.coord == piece.coord:
                        if self.player == piece.player.opponent():
                            self.captures.add(square)
                        break
                else:
                    self.captures.add(square)
                    continue
                break

    def remove_xray_defended_squares(self) -> None:
        """
        Removes xray defended squares from legal moves and captures
        """
        for attacker in game.king_attackers:
            attacker : Piece
            for direction in attacker.directions:
                for square in attacker.move_square_generator(direction):
                    if square in self.legal_moves:
                        self.legal_moves.remove(square)
                    if square in self.captures:
                        self.captures.remove(square)

    def update_moves_after_check(self) -> None:
        """
        Updates King possible moves and captures after Check
        """
        self.update_legal_moves()
        self.update_captures()
        self.remove_xray_defended_squares()

    def move(self, square: Square) -> None:
        """
        Extends super implementation by
        marking the King if moved.
        """
        self.moved = True
        return super().move(square)
