import pygame

from pygame import Rect
from pygame.sprite import AbstractGroup
from pygame.surface import Surface
from typing import *

import utils

from board.coord import Coord
from board.square import Square
from game import *
from pieces.captures import WhiteCaptures, BlackCaptures
from pieces.moves import WhiteMoves, BlackMoves
from settings import Settings


class Piece(Square):
    """
    Abstract class for every piece
    """

    move_range = 0
    directions: set[Coord] = set()

    def __init__(self, coord: Coord, is_white: bool, *groups: AbstractGroup) -> None:
        super().__init__(coord, *groups)
        self.is_white = is_white
        self.player = Player.WHITE if is_white else Player.BLACK
        self.possible_moves = WhiteMoves() if is_white else BlackMoves()
        self.possible_captures = WhiteCaptures() if is_white else BlackCaptures()
        self.image = self.get_image()
        self.rect = self.get_rect()

    def setup(self) -> None:
        self.possible_moves.owner = self
        self.possible_captures.owner = self
        self.update_possible_moves_and_captures()

    def draw(self, surface: Surface) -> None:
        # Ensures that Square.draw is overridden
        pass

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)

    def move_square_generator(self, direction: Coord) -> Square:
        """
        Generator for Piece moves in specified direction
        """
        for i in range(1, self.move_range + 1):
            for square in game.squares:
                if not isinstance(square, Square):
                    continue
                if square.coord == (direction * Coord(i, i) + self.coord):
                    yield square

    def update_possible_moves_and_captures(self) -> None:
        """
        Updates Piece possible moves and captures
        """
        self.update_possible_moves()
        self.update_possible_captures()

    def update_possible_moves(self) -> None:
        """
        Updates Piece possible moves according to move_square_generator
        """
        self.possible_moves.empty()

        for direction in self.directions:
            for square in self.move_square_generator(direction):
                for piece in game.pieces:
                    if not isinstance(piece, Piece):
                        continue
                    if square.coord == piece.coord:
                        break
                else:
                    self.possible_moves.add(square)
                    continue
                break

    def update_possible_captures(self) -> None:
        """
        Updates Piece possible captures according to move_square_generator
        """
        self.possible_captures.empty()

        for direction in self.directions:
            for square in self.move_square_generator(direction):
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

    def update_possible_moves_and_captures_after_check(self) -> None:
        """
        Updates Piece possible moves and captures after Check
        """
        self.update_possible_moves_after_check()
        self.update_possible_captures_after_check()

    def update_possible_moves_after_check(self) -> None:
        """
        Updates Piece possible moves after Check
        """
        # If multiple attackers then only King can move
        if len(game.king_attackers) > 1:
            self.possible_moves.empty()
            return

        # If Knight checks then only King can move
        if game.is_knight_king_attacker:
            self.possible_moves.empty()
            return

        # TODO: Implement more update moves after Check

    def update_possible_captures_after_check(self) -> None:
        """
        Updates Piece possible captures after Check
        """
        # If multiple attackers then only King can move
        if len(game.king_attackers) > 1:
            self.possible_captures.empty()
            return

        # If Knight checks then can only capture Knight
        if game.is_knight_king_attacker:
            knight : Piece = game.king_attackers.sprites()[0]
            for possible_capture in self.possible_captures:
                if not isinstance(possible_capture, Square):
                    continue
                if possible_capture.coord != knight.coord:
                    self.possible_captures.remove(possible_capture)

        # TODO: Implement more update captures after Check

    def get_image(self) -> Surface:
        """
        Gets the sprite image according to Piece name and color
        """
        # Loading image with both white and black piece
        name = self.__class__.__name__.lower()
        image = utils.load_image(utils.join(Settings.PIECES_IMG_DIR, f'{name}.png'))

        # Cropping the piece with appropriate color
        (width, height) = image.get_size()
        offset = 0 if self.is_white else -height/2
        cropped = pygame.Surface((width, height/2), pygame.SRCALPHA).convert_alpha()
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
        pass

    def move(self, square: Square) -> None:
        """
        Moves the Piece to desired square
        """
        self.coord = square.coord
        self.full_rect = self.get_full_rect()
        self.rect = self.get_rect()
