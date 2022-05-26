import os
import pygame

from pygame import Rect
from pygame.sprite import AbstractGroup
from pygame.surface import Surface
from typing import *

from board.square import Square
from game import *
from settings import Settings


class Piece(Square):
    """
    Abstract class for every piece
    """

    pieces_img_dir = os.path.join('img', 'pieces')

    def __init__(self, row: int, col: int, is_white: bool, *groups: AbstractGroup) -> None:
        super().__init__(row, col, *groups)
        self.is_white = is_white
        self.player = Player.WHITE if is_white else Player.BLACK
        self.background_color = Settings.black_piece_color if is_white else Settings.white_piece_color
        self.image = self.get_image()
        self.rect = self.get_rect()

    def draw(self, surface: Surface) -> None:
        # Ensures that Square.draw is overridden
        pass

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)

    def get_image(self) -> Surface:
        """
        Gets the sprite image according to piece name and color
        """
        # Loading image with both white and black piece
        name = self.__class__.__name__.lower()
        image_path = os.path.join(self.pieces_img_dir, f'{name}.png')
        image = pygame.image.load(image_path).convert_alpha()

        # Cropping the piece with appropriate color
        (width, height) = image.get_size()
        offset = 0 if self.is_white else -height/2
        cropped = pygame.Surface((width, height/2), pygame.SRCALPHA).convert_alpha()
        cropped.blit(image, (0, offset))

        # Scaling image to square size
        image = pygame.transform.smoothscale(cropped, Settings.square_size)
        return image

    def get_rect(self) -> Rect:
        return self.image.get_rect(center=self.full_rect.center)

    def move(self, row_i: int, col_i: int) -> None:
        """
        Moves a Piece to desired row and col
        """
        self.row_i = row_i
        self.col_i = col_i
        self.full_rect = self.get_full_rect()
        self.rect = self.get_rect()
