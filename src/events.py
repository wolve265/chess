import pygame

# NEXT_ACTION is a dummy event which forces next action
NEXT_ACTION = pygame.event.custom_type()
END_GAME = pygame.event.custom_type()

def gen_event(event: int) -> None:
    """
    Generates the pygame event
    """
    pygame.event.post(pygame.event.Event(event))
