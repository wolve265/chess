from pygame.sprite import Group, Sprite
from typing import *


class Captures(Group):
    def __init__(self, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        self.owner = None

    def __repr__(self) -> str:
        return f"{self.owner} has {super().__repr__()}"


class WhiteCaptures(Captures):
    pass


class BlackCaptures(Captures):
    pass
