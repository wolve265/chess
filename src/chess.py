import pygame as pg

from board.chessboard import Board
from events import END_APP, END_GAME, MAIN_MENU, START_GAME, gen_event
from game import game
from popup.endgame import EndGamePopupGroup
from popup.startgame import StartGamePopupGroup
from settings import Settings


class Chess:
    """
    Class used as a wrapper
    """

    def __init__(self) -> None:
        self.running = False
        self.board = Board()
        self.start_popup = StartGamePopupGroup()
        self.end_popup = EndGamePopupGroup()
        self.groups = [
            self.board,
            self.start_popup,
            self.end_popup,
        ]

    def run(self) -> None:
        self.running = True
        gen_event(MAIN_MENU)
        while self.running:
            self.actions()
            self.update()
            pg.display.update()
            game.clock.tick(Settings.FPS)
        pg.quit()

    def actions(self) -> None:
        """
        Main game logic
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == MAIN_MENU:
                self.board.active = False
                self.end_popup.active = False
                self.start_popup.active = True
            elif event.type == START_GAME:
                self.board.restart()
                self.board.active = True
                self.start_popup.active = False
            elif event.type == END_GAME:
                self.board.active = False
                self.end_popup.active = True
            elif event.type == END_APP:
                self.running = False
            # NOTE: Only active groups would work
            for group in self.groups:
                group.actions(event)

    def update(self) -> None:
        """
        Updates and draws every group
        """
        for group in self.groups:
            group.update()
            group.draw(game.screen)
