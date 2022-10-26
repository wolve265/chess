from pygame.sprite import AbstractGroup

from board.coord import Coord
from board.square import Square
from game import game
from pieces.piece import Piece
from pieces.rook import Rook


class King(Piece):
    """
    Class representing the King piece
    """

    move_range = 1
    directions = {
        Coord(1, 0),
        Coord(1, 1),
        Coord(0, 1),
        Coord(-1, 1),
        Coord(-1, 0),
        Coord(-1, -1),
        Coord(0, -1),
        Coord(1, -1),
    }

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
            for square in self.move_square_generator(direction):
                if self.player.opponent() in square.defended_by:
                    break
                for piece in game.pieces:
                    if not isinstance(piece, Piece):
                        continue
                    if square.coord == piece.coord:
                        break
                else:
                    self.legal_moves.add(square)
        self.update_castling_moves()

    def update_castling_moves(self) -> None:
        """
        Extending legal moves by castling moves
        """
        # Cannot castle if King is checked
        if game.state.check:
            return
        # Cannot castle if King moved
        if self.moved:
            return
        # Find Rooks in the King's row that the King can castle with
        for rook in self.get_row():
            if not isinstance(rook, Rook):
                continue
            # Cannot castle if Rook moved
            if rook.moved:
                continue
            vector = rook.coord - self.coord
            move_range = abs(vector.col_i) - 1  # one square before Rook
            direction = vector.get_direction()
            king_dst_coord = direction * Coord(1, 2) + self.coord
            dst_square: Square | None = None
            piece_found = False
            for i, square in enumerate(self.move_square_generator(direction, move_range), 1):
                if i != move_range and self.player.opponent() in square.defended_by:
                    break
                for piece in game.pieces:
                    if not isinstance(piece, Piece):
                        continue
                    if square.coord == piece.coord:
                        piece_found = True
                        break
                if piece_found:
                    break
                if square.coord == king_dst_coord:
                    dst_square = square
            if dst_square and not piece_found:
                self.legal_moves.add(dst_square)

    def update_captures(self) -> None:
        """
        Overrides super class implementation.
        King can't capture the defended piece.
        """
        for direction in self.directions:
            for square in self.move_square_generator(direction):
                if self.player.opponent() in square.defended_by:
                    continue
                for piece in game.pieces:
                    if not isinstance(piece, Piece):
                        continue
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
            if not isinstance(attacker, Piece):
                continue
            coord = self.coord - attacker.coord
            direction = coord.get_direction()
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
