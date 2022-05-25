import os
import pygame

from pygame.sprite import AbstractGroup
from pygame.surface import Surface
from typing import *

from board.square import Square
from settings import Settings


class Piece(Square):
    """
    Abstract class for every piece
    """

    pieces_img_dir = os.path.join('img', 'pieces')

    def __init__(self, row: int, col: int, is_white: bool, *groups: AbstractGroup) -> None:
        super().__init__(row, col, *groups)
        self.is_white = is_white
        self.color = Settings.white_piece_color if is_white else Settings.black_piece_color
        self.background_color = Settings.black_piece_color if is_white else Settings.white_piece_color
        self.image = self.get_image()
        self.rect = self.image.get_rect(center=self.full_rect.center)

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
