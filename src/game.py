import sys
from dataclasses import dataclass
from enum import Enum, auto

import pygame as pg
from pygame.sprite import AbstractGroup

from settings import Settings


class Player(Enum):
    WHITE = 1
    BLACK = 0

    def __str__(self) -> str:
        return f"Player {self.name.capitalize()}"

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

    @property
    def end(self) -> bool:
        return self.checkmate or self.stalemate


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
        self.counter = 1
        self.turn_counter = 1

    def update_at_start_turn(self) -> None:
        game.state.capture = False
        game.state.short_castle = False
        game.state.long_castle = False

    def end_player_turn(self, move_notation: str = "") -> None:
        """
        Ends player turn
        """
        if self.counter % 2:
            sys.stdout.write(f"\n{self.turn_counter:>3}.")
            self.turn_counter += self.counter % 2
        sys.stdout.write(f" {move_notation}")
        sys.stdout.flush()
        if not self.state.end:
            self.counter += 1
            self.state.player = self.state.player.opponent()

    def end_game(self) -> None:
        """
        Prints end game result
        """
        sys.stdout.write(f"\n{self.state.player} wins")


game = Game()
