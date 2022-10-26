from collections.abc import Sequence
from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface

import utils

from game import game
from settings import Settings


class Row(Group):
    """
    Class representing the board row
    """

    def __init__(self, row_i: int, *sprites: Sprite | Sequence[Sprite]) -> None:
        super().__init__(*sprites)
        self.row_i = row_i
        self.row_str = utils.row_int2str(self.row_i)
        self.full_rect_left = Rect(
            (0, (Settings.ROW_NUM - self.row_i - 1) * Settings.SQUARE_LEN + Settings.BORDER_LEN),
            (Settings.BORDER_LEN, Settings.SQUARE_LEN),
        )
        self.full_rect_right = Rect(
            (
                Settings.BOARD_LEN + Settings.BORDER_LEN,
                (Settings.ROW_NUM - self.row_i - 1) * Settings.SQUARE_LEN + Settings.BORDER_LEN,
            ),
            (Settings.BORDER_LEN, Settings.SQUARE_LEN),
        )
        self.image = game.font.render(f"{self.row_str}", True, Settings.SQUARE_WHITE_COLOR)
        self.rect_left = self.image.get_rect(center=self.full_rect_left.center)
        self.rect_right = self.image.get_rect(center=self.full_rect_right.center)

    def __repr__(self) -> str:
        return f"{super().__repr__()} = {self.row_i}"

    def draw(self, surface: Surface) -> list[Rect]:
        surface.blit(self.image, self.rect_left)
        surface.blit(self.image, self.rect_right)
        return super().draw(surface)
