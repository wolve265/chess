import pygame as pg
from pygame.event import Event

# NEXT_ACTION is a dummy event which forces next action
NEXT_ACTION = pg.event.custom_type()
MAIN_MENU = pg.event.custom_type()
START_GAME = pg.event.custom_type()
END_GAME = pg.event.custom_type()
END_APP = pg.event.custom_type()


def gen_event(event: int) -> None:
    """
    Generates the pygame event
    """
    pg.event.post(Event(event))
