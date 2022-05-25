import pygame

from board.chessboard import Board
from game import game
from settings import Settings


class Chess:
    """
    Class representing the chess game
    """

    def __init__(self) -> None:
        self.running = False
        self.board = Board()

    def run(self) -> None:
        self.running = True
        while self.running:
            self.actions()
            self.update()
            pygame.display.update()
            game.clock.tick(Settings.fps)
        pygame.quit()

    def actions(self) -> None:
        """
        Main game logic
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self) -> None:
        """
        Updates and draws every group
        """
        self.board.update()
        self.board.draw(game.screen)
