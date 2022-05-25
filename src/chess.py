import pygame

from board.chessboard import Board
from game import game
from settings import Settings


class Chess:

    def __init__(self) -> None:
        self.running = False
        self.board = Board()
        # print(self.board.sprites())
        # print(self.board.rows[0].sprites())

    def run(self) -> None:
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.board.update()
            self.board.draw(game.screen)

            pygame.display.update()
            game.clock.tick(Settings.fps)

        pygame.quit()
