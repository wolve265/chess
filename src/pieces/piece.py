from collections.abc import Iterator
from typing import Any

import pygame
from pygame.rect import Rect
from pygame.sprite import AbstractGroup
from pygame.surface import Surface

import utils
from board.coord import Coord
from board.square import Square
from game import Player, game
from pieces.moves import (
    BlackCaptures,
    BlackDefendedSquares,
    BlackLegalMoves,
    WhiteCaptures,
    WhiteDefendedSquares,
    WhiteLegalMoves,
)
from settings import Settings


class Piece(Square):
    """
    Abstract class for every piece
    """

    move_range = 0
    directions: set[Coord] = set()

    def __init__(self, coord: Coord, is_white: bool, *groups: AbstractGroup) -> None:
        super().__init__(coord, *groups)
        self.start_coord = coord
        self.id = self.__class__.__name__[0]
        self.is_white = is_white
        self.player = Player.WHITE if is_white else Player.BLACK
        self.legal_moves = WhiteLegalMoves() if is_white else BlackLegalMoves()
        self.captures = WhiteCaptures() if is_white else BlackCaptures()
        self.defended_squares = WhiteDefendedSquares() if is_white else BlackDefendedSquares()
        self.image = self.get_image()
        self.rect = self.get_rect()

        # Flags
        self.pinned_directions: set[Coord] = set()
        self.pinned = False

    def setup(self) -> None:
        self.legal_moves.owner.add(self)
        self.captures.owner.add(self)
        self.update_moves()

    def draw(self, surface: Surface) -> None:
        # Ensures that Square.draw is overridden
        pass

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)

    def kill(self) -> None:
        self.legal_moves.empty()
        self.captures.empty()
        self.defended_squares.empty()
        return super().kill()

    def move_square_generator(
        self, direction: Coord, move_range: int | None = None
    ) -> Iterator[Square]:
        """
        Generator for Piece moves in specified direction
        """
        move_range = move_range if move_range is not None else self.move_range
        for i in range(1, move_range + 1):
            for square in game.squares:
                if not isinstance(square, Square):
                    continue
                if square.coord == (direction * Coord(i, i) + self.coord):
                    yield square

    def update_moves(self) -> None:
        """
        Updates Piece moves:
        - legal moves
        - captures
        - defended squares
        """
        self.legal_moves.empty()
        self.captures.empty()
        self.defended_squares.empty()
        self.update_legal_moves()
        self.update_captures()
        self.update_defended_squares()

    def update_legal_moves(self) -> None:
        """
        Updates Piece legal moves according to move_square_generator
        """
        for direction in self.directions:
            if self.pinned and direction not in self.pinned_directions:
                continue
            for square in self.move_square_generator(direction):
                for piece in game.pieces:
                    if not isinstance(piece, Piece):
                        continue
                    if square.coord == piece.coord:
                        break
                else:
                    self.legal_moves.add(square)
                    continue
                break

    def update_captures(self) -> None:
        """
        Updates Piece possible captures according to move_square_generator
        """
        for direction in self.directions:
            if self.pinned and direction not in self.pinned_directions:
                continue
            for square in self.move_square_generator(direction):
                for piece in game.pieces:
                    if not isinstance(piece, Piece):
                        continue
                    if square.coord == piece.coord:
                        if self.player == piece.player.opponent():
                            self.captures.add(square)
                        break
                else:
                    continue
                break

    def update_defended_squares(self) -> None:
        """
        Updates Piece defended squares according to move_square_generator
        """
        for direction in self.directions:
            for square in self.move_square_generator(direction):
                for piece in game.pieces:
                    if not isinstance(piece, Piece):
                        continue
                    if square.coord == piece.coord:
                        self.defended_squares.add(square)
                        break
                else:
                    self.defended_squares.add(square)
                    continue
                break

    def update_moves_after_check(self) -> None:
        """
        Updates Piece moves after Check:
        - legal moves
        - captures
        """
        self.update_legal_moves_after_check()
        self.update_captures_after_check()

    def update_legal_moves_after_check(self) -> None:
        """
        Updates Piece possible moves after Check
        """
        # If multiple attackers then only King can move
        if len(game.king_attackers) > 1:
            self.legal_moves.empty()
            return
        if self.player == game.state.player:
            return

        # Only blocking moves are allowed
        for legal_move in self.legal_moves:
            if not isinstance(legal_move, Square):
                continue
            block_coords: list[Coord] = []
            for block_move in game.squares_between_king_and_attacker:
                if not isinstance(block_move, Square):
                    continue
                block_coords.append(block_move.coord)
            if legal_move.coord not in block_coords:
                self.legal_moves.remove(legal_move)

    def update_captures_after_check(self) -> None:
        """
        Updates Piece possible captures after Check
        """
        # If multiple attackers then capture is not allowed (King is handled by different function)
        king_attackers: list[Piece] = [
            sprite for sprite in game.king_attackers if isinstance(sprite, Piece)
        ]
        if len(king_attackers) > 1:
            self.captures.empty()
            return
        # Only the capture of the attacker Piece is allowed
        attacker = king_attackers[0]
        for capture in self.captures:
            if not isinstance(capture, Square):
                continue
            if capture.coord != attacker.coord:
                self.captures.remove(capture)

    def get_image(self) -> Surface:
        """
        Gets the sprite image according to Piece name and color
        """
        # Loading image with both white and black piece
        name = self.__class__.__name__.lower()
        image = utils.load_image(utils.join(Settings.PIECES_IMG_DIR, f"{name}.png"))

        # Cropping the piece with appropriate color
        (width, height) = image.get_size()
        offset = 0 if self.is_white else -height / 2
        cropped = pygame.Surface((width, height / 2), pygame.SRCALPHA).convert_alpha()
        cropped.blit(image, (0, offset))

        # Scaling image to square size
        image = pygame.transform.smoothscale(cropped, Settings.SQUARE_SIZE)
        return image

    def get_rect(self) -> Rect:
        return self.image.get_rect(center=self.full_rect.center)

    def update_flags(self) -> None:
        """
        Updates the Piece flags
        """
        self.pinned_directions.clear()
        self.pinned = False

    def move(self, square: Square) -> None:
        """
        Moves the Piece to desired square
        """
        row, col = self.get_row_col()
        row.remove(self)
        col.remove(self)
        self.coord = square.coord
        self.full_rect = self.get_full_rect()
        self.rect = self.get_rect()
        row, col = square.get_row_col()
        row.add(self)
        col.add(self)
