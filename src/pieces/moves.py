from pygame.sprite import Group, Sprite
from typing import *

class Moves(Group):
    def __init__(self, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        self.owner = None

    def __repr__(self) -> str:
        return f"{self.owner} has {super().__repr__()}"


class WhiteMoves(Moves):
    pass


class BlackMoves(Moves):
    pass
