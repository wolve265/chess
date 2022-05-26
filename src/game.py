import pygame

from dataclasses import dataclass
from enum import Enum, auto

from settings import Settings


class Player(Enum):
    WHITE = auto()
    BLACK = auto()


class Action(Enum):
    SELECT = auto()
    PLACE = auto()


@dataclass
class State:
    player: Player = Player.WHITE
    action: Action = Action.SELECT


class Game:
    """
    Class representing the game
    """

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(Settings.window_caption)
        self.screen = pygame.display.set_mode(Settings.window_size)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, Settings.font_size)
        self.state = State()
        print(self.state)

game = Game()
