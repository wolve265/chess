import pygame

from board import Board
from game import game


class Chess:

    def __init__(self) -> None:
        self.running = False
        self.board = Board()
        print(self.board.sprites())

    def run(self) -> None:
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.board.update()
            self.board.draw(game.screen)

            pygame.display.update()
            game.clock.tick(60)

        pygame.quit()
