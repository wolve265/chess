import pygame

from dataclasses import dataclass
from enum import Enum, auto

from settings import Settings


class Player(Enum):
    WHITE = auto()
    BLACK = auto()


class Action(Enum):
    SELECT = auto()
    MOVE = auto()
    END_TURN = auto()


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

    def end_player_turn(self) -> None:
        """
        Ends player turn
        """
        if self.state.player == Player.WHITE:
            self.state.player = Player.BLACK
        else:
            self.state.player = Player.WHITE

game = Game()
