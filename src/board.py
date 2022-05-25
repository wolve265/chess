import pygame

from itertools import product
from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface
from typing import *

from game import game
from square import Square
from settings import Settings


class Board(Group):
    def __init__(self, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        self.squares: List[Square] = []
        self.rows: List[Row] = []
        self.cols: List[Col] = []
        self.gen_squares()
        super().__init__(self.squares, *sprites)

    def draw(self, surface: Surface) -> List[Rect]:
        game.screen.fill(Settings.background_color)
        for square in self.squares:
            square.draw(surface)
        for row, col in zip(self.rows, self.cols):
            row.draw(surface)
            col.draw(surface)
        return super().draw(surface)

    def update(self, *args: Any, **kwargs: Any) -> None:
        return super().update(*args, **kwargs)

    def gen_squares(self) -> List[Sprite]:
        for i in range(Settings.rows):
            self.rows.append(Row(i))
            self.cols.append(Col(i))
        for row_i in range(Settings.rows):
            for col_i in range(Settings.cols):
                self.squares.append(Square(row_i, col_i, self.rows[row_i], self.cols[col_i]))


class Row(Group):
    def __init__(self, row, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        self.row = row
        self.row_str = chr(self.row + ord('1'))
        self.full_rect_left = pygame.Rect((0, (Settings.rows-self.row-1)*Settings.square_len + Settings.border_len), (Settings.border_len, Settings.square_len))
        self.full_rect_right = pygame.Rect((Settings.board_len + Settings.border_len, (Settings.rows-self.row-1)*Settings.square_len + Settings.border_len), (Settings.border_len, Settings.square_len))
        self.image = game.font.render(f"{self.row_str}", True, Settings.white_color)
        self.rect_left = self.image.get_rect(center=self.full_rect_left.center)
        self.rect_right = self.image.get_rect(center=self.full_rect_right.center)

    def __repr__(self) -> str:
        return f'{super().__repr__()} = {self.row}'

    def draw(self, surface: Surface) -> List[Rect]:
        surface.blit(self.image, self.rect_left)
        surface.blit(self.image, self.rect_right)
        return super().draw(surface)


class Col(Group):
    def __init__(self, col, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        self.col = col
        self.col_str = chr(self.col + ord('a'))
        self.full_rect_top = pygame.Rect((self.col*Settings.square_len + Settings.border_len, 0), (Settings.square_len, Settings.border_len))
        self.full_rect_bottom = pygame.Rect((self.col*Settings.square_len + Settings.border_len, Settings.board_len + Settings.border_len), (Settings.square_len, Settings.border_len))
        self.image = game.font.render(f"{self.col_str}", True, Settings.white_color)
        self.rect_top = self.image.get_rect(center=self.full_rect_top.center)
        self.rect_bottom = self.image.get_rect(center=self.full_rect_bottom.center)

    def __repr__(self) -> str:
        return f'{super().__repr__()} = {self.col}'

    def draw(self, surface: Surface) -> List[Rect]:
        surface.blit(self.image, self.rect_top)
        surface.blit(self.image, self.rect_bottom)
        return super().draw(surface)
