import pygame

from board.chessboard import Board
from events import *
from game import *
from settings import Settings


class Chess:
    """
    Class used as a wrapper
    """

    def __init__(self) -> None:
        self.running = False
        self.board = Board()
        self.cnt = 0

    def run(self) -> None:
        self.running = True
        while self.running:
            self.actions()
            self.update()
            pygame.display.update()
            game.clock.tick(Settings.FPS)
        pygame.quit()

    def actions(self) -> None:
        """
        Main game logic
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == END_GAME:
                input("Press any key to exit")
                self.running = False
            else:
                self.board.actions(event)

    def update(self) -> None:
        """
        Updates and draws every group
        """
        self.board.update()
        self.board.draw(game.screen)
