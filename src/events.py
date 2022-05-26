import pygame

END_GAME = pygame.event.custom_type()

def gen_event(event: pygame.event.Event) -> None:
    """
    Generates the pygame event
    """
    pygame.event.post(pygame.event.Event(event))
