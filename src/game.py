import pygame

from dataclasses import dataclass
from enum import Enum, auto
from pygame.sprite import AbstractGroup

from settings import Settings


class Player(Enum):
    WHITE = 1
    BLACK = 0

    def opponent(self) -> 'Player':
        return Player(not self.value)


class Action(Enum):
    SELECT = auto()
    MOVE = auto()
    END_TURN = auto()


@dataclass
class State:
    player: Player = Player.WHITE
    action: Action = Action.SELECT
    check: bool = False
    checkmate: bool = False


class Game:
    """
    Class representing the game
    """

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(Settings.WINDOW_CAPTION)
        self.screen = pygame.display.set_mode(Settings.WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, Settings.FONT_SIZE)
        self.state = State()
        self.turn_counter = 1
        self.squares = AbstractGroup()
        self.pieces = AbstractGroup()
        self.king_attackers = AbstractGroup()
        self.is_knight_king_attacker = False

    def end_player_turn(self) -> None:
        """
        Ends player turn
        """
        self.turn_counter += 1
        if self.state.player == Player.WHITE:
            self.state.player = Player.BLACK
        else:
            self.state.player = Player.WHITE

game = Game()
