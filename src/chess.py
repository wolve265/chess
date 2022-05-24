import pygame

from game import Game


class Chess:

    def __init__(self) -> None:
        self.running = False

    def run(self) -> None:
        game = Game()
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.update()
            game.clock.tick(60)

        pygame.quit()
