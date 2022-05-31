import time
import pygame

from pygame import Rect
from pygame.sprite import AbstractGroup
from pygame.surface import Surface
from typing import *

import utils

from board.coord import Coord
from board.square import Square
from game import *
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
        self.background_color = Settings.BLACK_COLOR if is_white else Settings.WHITE_COLOR
        self.moves: set[Coord] = set()
        self.possible_moves = AbstractGroup()
        self.image = self.get_image()
        self.rect = self.get_rect()
        self.setup()

    def setup(self) -> None:
        self.update_moves()
        self.update_possible_moves()

    def draw(self, surface: Surface) -> None:
        # Ensures that Square.draw is overridden
        pass

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)

    def update_moves(self) -> None:
        """
        Updates moves
        """
        self.moves = set()
        for direction in self.directions:
            for i in range(1, self.move_range+1):
                self.moves.add(direction * Coord(i, i))

    def update_possible_moves(self) -> None:
        """
        Updates possible moves
        """
        self.possible_moves.empty()

        for square in game.squares:
            if (square.coord - self.coord) in self.moves:
                self.possible_moves.add(square)

    def get_image(self) -> Surface:
        """
        Gets the sprite image according to piece name and color
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

    def move(self, square: Square) -> None:
        """
        Moves a Piece to desired square
        """
        self.coord = square.coord
        self.full_rect = self.get_full_rect()
        self.rect = self.get_rect()
        self.update_possible_moves()
