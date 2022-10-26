import pygame as pg

from dataclasses import dataclass
from enum import Enum, auto
from pygame.sprite import AbstractGroup

from settings import Settings


class Player(Enum):
    WHITE = 1
    BLACK = 0

    def opponent(self) -> "Player":
        return Player(not self.value)


class Action(Enum):
    SELECT = auto()
    MOVE = auto()
    END_TURN = auto()


@dataclass
class State:
    player: Player = Player.BLACK
    action: Action = Action.SELECT
    short_castle: bool = False
    long_castle: bool = False
    capture: bool = False
    check: bool = False
    checkmate: bool = False
    stalemate: bool = False


class Game:
    """
    Class representing the game
    """

    def __init__(self) -> None:
        pg.init()
        pg.display.set_caption(Settings.WINDOW_CAPTION)
        self.screen = pg.display.set_mode(Settings.WINDOW_SIZE)
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, Settings.FONT_SIZE)
        self.state = State()
        self.counter = -1
        self.turn_counter = 0
        self.squares = AbstractGroup()
        self.pieces = AbstractGroup()
        self.king_attackers = AbstractGroup()
        self.squares_between_king_and_attacker = AbstractGroup()
        self.is_knight_king_attacker = False

    def setup(self) -> None:
        """
        Sets up game
        """
        self.state.player = Player.WHITE
        self.counter = 0
        self.turn_counter = 1
        print(f"{self.turn_counter:>3}.", end=" ")

    def update_at_start_turn(self) -> None:
        game.state.capture = False
        game.state.short_castle = False
        game.state.long_castle = False

    def end_player_turn(self, move_notation: str = "") -> None:
        """
        Ends player turn
        """
        print(f"{move_notation:5}", end=" ")
        if self.counter % 2:
            self.turn_counter += self.counter % 2
            print(f"\n{self.turn_counter:>3}.", end=" ")
        self.counter += 1
        self.state.player = self.state.player.opponent()


game = Game()
