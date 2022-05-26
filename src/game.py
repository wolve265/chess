import pygame

from settings import Settings


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


game = Game()
