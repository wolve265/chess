import pygame

from settings import Settings

class Game:

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(Settings.window_caption)
        self.screen = pygame.display.set_mode((Settings.board_len, Settings.board_len))
        self.clock = pygame.time.Clock()
