from collections.abc import Sequence

from pygame.sprite import Group, GroupSingle, Sprite


class Moves(Group):
    def __init__(self, *sprites: Sprite | Sequence[Sprite]) -> None:
        super().__init__(*sprites)
        self.owner = GroupSingle()

    def __repr__(self) -> str:
        return f"{self.owner} has {super().__repr__()}"


class WhiteLegalMoves(Moves):
    ...


class BlackLegalMoves(Moves):
    ...


class WhiteCaptures(Moves):
    ...


class BlackCaptures(Moves):
    ...


class WhiteDefendedSquares(Moves):
    ...


class BlackDefendedSquares(Moves):
    ...
