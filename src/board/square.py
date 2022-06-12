import pygame

from pygame import Rect
from pygame.color import Color
from pygame.sprite import AbstractGroup, Sprite
from pygame.surface import Surface
from typing import *

import utils

from board.col import Col
from board.row import Row
from board.coord import Coord
from game import *
from settings import Settings


class Square(Sprite):
    """
    Class representing the single square of the chessboard
    """

    possible_move_image = utils.load_image(utils.join(Settings.IMG_DIR, 'possible_move.png'))
    possible_capture_image = utils.load_image(utils.join(Settings.IMG_DIR, 'possible_capture.png'))

    def __init__(self, coord: Coord, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.coord = coord
        self.color = self.get_color()
        self.full_rect = self.get_full_rect()
        self.image = game.font.render(f"", True, Settings.BLACK_COLOR)
        self.rect = self.image.get_rect(center=self.full_rect.center)
        self.checked_by = set()

    def __repr__(self) -> str:
        return f'\n{super().__repr__()} | coord = ({self.coord})'

    def draw(self, surface: Surface) -> None:
        pygame.draw.rect(surface, self.color, self.full_rect)

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)

    def get_color(self) -> Color:
        return Settings.SQUARE_WHITE_COLOR if (self.coord.row_i + self.coord.col_i) % 2 else Settings.SQUARE_BLACK_COLOR

    def get_full_rect(self) -> Rect:
        return pygame.Rect((self.coord.col_i*Settings.SQUARE_LEN + Settings.BORDER_LEN, (Settings.ROW_NUM-self.coord.row_i-1)*Settings.SQUARE_LEN + Settings.BORDER_LEN), Settings.SQUARE_SIZE)

    def get_row_group(self) -> Row:
        for group in self.groups():
            if isinstance(group, Row):
                return group

    def get_col_group(self) -> Col:
        for group in self.groups():
            if isinstance(group, Col):
                return group

    def render_selection(self) -> None:
        self.color = utils.highlight_color(self.color)

    def render_possible_move(self) -> None:
        self.image = self.possible_move_image
        self.rect = self.image.get_rect(center=self.full_rect.center)

    def render_possible_capture(self) -> None:
        self.image = self.possible_capture_image
        self.rect = self.image.get_rect(center=self.full_rect.center)

    def render_reset(self) -> None:
        self.color = self.get_color()
        self.image = game.font.render(f"", True, Settings.BLACK_COLOR)
        self.rect = self.image.get_rect(center=self.full_rect.center)
